import os
import re
import shutil
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
import subprocess
import tempfile
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pugify")

app = Flask(__name__)

# Configuration
FFMPEG_PATH = None
SPOTIFY_TRACK_REGEX = r'^https?://open\.spotify\.com(?:/intl-[a-z]{2})?/track/[a-zA-Z0-9]+(\?.*)?$'

# Initialize FFmpeg path
def initialize_ffmpeg():
    """Initialize FFmpeg path - static binary or system."""
    global FFMPEG_PATH
    
    # Try static binary first
    static_paths = [
        './ffmpeg_bin/ffmpeg',
        '/app/ffmpeg_bin/ffmpeg',
        'ffmpeg_bin/ffmpeg',
    ]
    
    for path in static_paths:
        if Path(path).exists():
            FFMPEG_PATH = os.path.abspath(path)
            logger.info(f"✓ Using static FFmpeg: {FFMPEG_PATH}")
            os.environ['LD_LIBRARY_PATH'] = os.path.dirname(FFMPEG_PATH)
            return
    
    # Fallback to system FFmpeg
    try:
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            FFMPEG_PATH = result.stdout.strip()
            logger.info(f"✓ Using system FFmpeg: {FFMPEG_PATH}")
            return
    except Exception as e:
        logger.warning(f"Could not find system FFmpeg: {e}")
    
    logger.warning("⚠ FFmpeg not found - downloads may fail")
    FFMPEG_PATH = 'ffmpeg'  # Assume it's in PATH


def is_valid_spotify_url(url):
    """Validate if URL is a valid Spotify track URL."""
    return re.match(SPOTIFY_TRACK_REGEX, url) is not None


def download_spotify_track(spotify_url):
    """
    Download track from Spotify using spotdl.
    Returns: (success: bool, file_path: str or error_message: str, track_name: str)
    """
    download_dir = None
    
    try:
        # Use system temp directory for better cleanup
        download_dir = tempfile.mkdtemp(prefix="spotfydown_")
        logger.info(f"📑 Download directory: {download_dir}")
        logger.info(f"🎧 Downloading: {spotify_url}")
        
        # Build spotdl command with FFmpeg
        cmd = [
            "spotdl",
            "--output",
            download_dir,
            "--format",
            "mp3",
            spotify_url
        ]
        
        # Add FFmpeg path if available
        env = os.environ.copy()
        if FFMPEG_PATH and FFMPEG_PATH != 'ffmpeg':
            env['PATH'] = f"{os.path.dirname(FFMPEG_PATH)}:{env.get('PATH', '')}"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            env=env
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error"
            logger.error(f"❌ Download failed: {error_msg}")
            return False, f"Download failed: {error_msg}", None
        
        # Find the downloaded MP3 file
        mp3_files = list(Path(download_dir).glob("*.mp3"))
        
        if not mp3_files:
            logger.error("❌ No MP3 file found after download")
            return False, "No MP3 file generated", None
        
        file_path = str(mp3_files[0])
        track_name = Path(file_path).stem
        
        logger.info(f"✅ Successfully downloaded: {track_name}")
        return True, file_path, track_name
        
    except subprocess.TimeoutExpired:
        logger.error("❌ Download timeout (5min exceeded)")
        return False, "Download took too long (max 5 minutes)", None
    except Exception as e:
        logger.error(f"❌ Download error: {str(e)}")
        return False, f"Error: {str(e)}", None
    finally:
        # Emergency cleanup if download failed
        if download_dir and Path(download_dir).exists():
            try:
                # Don't cleanup here - let the main route handle it
                pass
            except Exception as e:
                logger.error(f"Cleanup error: {e}")


def cleanup_temp_directory(directory_path):
    """Rigorously cleanup temporary directory and all contents."""
    try:
        if directory_path and Path(directory_path).exists():
            shutil.rmtree(directory_path, ignore_errors=True)
            logger.info(f"🗑 Cleaned up: {directory_path}")
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")


def cleanup_file(file_path):
    """Remove a single file and its parent directory if empty."""
    try:
        if not file_path:
            return
        
        file_obj = Path(file_path)
        if file_obj.exists():
            file_obj.unlink()
            logger.info(f"🗑 Deleted file: {file_path}")
            
            # Try to remove parent directory
            parent_dir = file_obj.parent
            try:
                parent_dir.rmdir()  # Only removes if empty
                logger.info(f"🗑 Deleted directory: {parent_dir}")
            except OSError:
                pass  # Directory not empty or other error, ignore
    except Exception as e:
        logger.error(f"File cleanup error: {str(e)}")


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/api/download", methods=["POST"])
def download():
    """API endpoint to download Spotify track."""
    download_dir = None
    file_path = None
    
    try:
        data = request.get_json()
        
        if not data or "url" not in data:
            return jsonify({"success": False, "error": "URL not provided"}), 400
        
        spotify_url = data["url"].strip()
        
        # Validate URL
        if not is_valid_spotify_url(spotify_url):
            return jsonify({
                "success": False,
                "error": "Invalid Spotify URL. Please provide a valid track link."
            }), 400
        
        # Download the track
        success, result, track_name = download_spotify_track(spotify_url)
        
        if not success:
            return jsonify({"success": False, "error": result}), 400
        
        file_path = result
        download_dir = str(Path(file_path).parent)
        
        # Prepare filename for download
        download_filename = f"{track_name}.mp3"
        logger.info(f"Sending file to client: {download_filename}")
        
        @after_this_request
        def cleanup_after_download(response):
            """Rigorous cleanup after file is sent to client."""
            import time
            # Give the response time to be sent
            time.sleep(0.5)
            cleanup_file(file_path)
            if download_dir and Path(download_dir).exists():
                cleanup_temp_directory(download_dir)
            logger.info("🗑 Cleanup completed")
            return response
        
        # Send file to user
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_filename,
            mimetype="audio/mpeg"
        )
    
    except Exception as e:
        logger.error(f"❌ API error: {str(e)}")
        # Try cleanup on error
        if file_path and Path(file_path).exists():
            cleanup_file(file_path)
        if download_dir and Path(download_dir).exists():
            cleanup_temp_directory(download_dir)
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "ffmpeg_path": FFMPEG_PATH
    }), 200


@app.before_request
def log_request():
    """Log incoming requests."""
    logger.info(f"{request.method} {request.path}")


if __name__ == "__main__":
    # Initialize FFmpeg
    initialize_ffmpeg()
    
    # Get port from environment variable, default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    
    logger.info(f"🚀 Starting Flask app on {host}:{port}")
    logger.info(f"💻 FFmpeg: {FFMPEG_PATH}")
    app.run(host=host, port=port, debug=False, threaded=True)
