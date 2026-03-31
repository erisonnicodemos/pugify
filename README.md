# 🎵 Pugify - MP3 Downloader

**A personal music production utility for converting Spotify tracks to MP3 for backing track creation and audio analysis**

---

## 🎯 Purpose & Context

Pugify is a **strictly personal-use web utility** designed to streamline my workflow as a musician. 

### The Problem:
Creating custom backing tracks and isolated audio tracks for practice requires:
1. Finding the original track on Spotify
2. Converting it to MP3 format
3. Importing it into music production software
4. Separating vocal, drums, bass, and other elements

### The Solution:
Pugify automates step 1-2, allowing me to quickly download Spotify tracks as MP3 files for use in **Moises** (a professional audio separation app), where I can:
- 🎙️ Isolate lead vocals for singing practice
- 🥁 Extract drum tracks for rhythm training  
- 🎸 Separate bass lines for accompaniment study
- 🎼 Create custom backing tracks with specific instruments
- 🎧 Remove vocals for karaoke-style practice

### Why Moises + Pugify?
Moises specializes in AI-powered audio stem separation. By feeding it high-quality MP3s from Spotify via Pugify, I can create professional-grade practice materials tailored to specific musical needs.

---

## ✨ Features

- ✅ **Simple Web Interface** - Paste a Spotify track URL, get an MP3
- ✅ **Production-Ready Backend** - Gunicorn WSGI server with multi-worker support
- ✅ **Static FFmpeg** - No system dependencies required (auto-detected or downloaded)
- ✅ **Rigorous File Cleanup** - Zero storage residue on the server
- ✅ **Real-Time Feedback** - Progress indicator & status messages during download
- ✅ **Render-Native** - Optimized for Render's ephemeral storage constraints
- ✅ **Responsive Design** - Works on desktop & mobile devices

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask + Gunicorn (WSGI) |
| **Frontend** | HTML5 + CSS3 + Bootstrap 5 (CDN) |
| **Audio Download** | spotdl + yt-dlp |
| **Audio Codec** | FFmpeg (static binary) |
| **Hosting** | Render (Python native, no Docker) |
| **Build** | Bash script (auto-detects x86_64/ARM64) |

---

## 🚀 Quick Start

### Local Setup

**Windows:**
```bash
cd c:\dev\pugify
setup.bat

gunicorn --workers 1 --threads 1 --worker-class gthread --bind 0.0.0.0:5000 app:app
# Open: http://localhost:5000
```

**Linux/macOS:**
```bash
cd ~/pugify
bash setup.sh

gunicorn --workers 1 --threads 1 --worker-class gthread --bind 0.0.0.0:5000 app:app
# Open: http://localhost:5000
```

### Using Pugify

1. Open a Spotify app and find a track
2. Click **"Share"** → **"Copy link to track"**
3. Paste the link into Pugify's input field
4. Click **"Download MP3"**
5. Your browser automatically downloads the file
6. Import the MP3 into Moises for stem separation

---

## 📋 Requirements

### System Requirements
- Python 3.9+
- FFmpeg (automatically downloaded during build, or use system version)

### Browser Compatibility
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 🔧 API Reference

### `GET /`
Returns the main web interface (HTML)

### `POST /api/download`
Downloads a Spotify track as MP3

**Request:**
```json
{
  "url": "https://open.spotify.com/track/11dFghVXANMlKmJXsNCQvb"
}
```

**Response (Success):**
- HTTP 200
- Content-Type: `audio/mpeg`
- File sent as attachment
- Automatic server-side cleanup after download

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid Spotify URL..."
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "ffmpeg_path": "/app/ffmpeg_bin/ffmpeg"
}
```

---

## 📁 Project Structure

```
pugify/
├── app.py                     # Flask backend with cleanup logic
├── templates/
│   └── index.html             # Web interface
├── requirements.txt           # Python dependencies
├── build.sh                   # Build script (FFmpeg static binary)
├── gunicorn.conf.py          # Gunicorn production config
├── render.yaml               # Render Blueprint deployment
├── setup.sh / setup.bat      # Local setup scripts
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore patterns
└── README.md                 # This file
```

---

## 🌐 Deployment

### Deploy on Render (Recommended)

```bash
# 1. Push to GitHub
git push origin main

# 2. On Render Dashboard
# New → Blueprint → Select repository → Deploy

# 3. Access your deployed app
# https://pugify-xxxx.onrender.com
```

### Using Render Blueprint

Pugify includes a `render.yaml` configuration that automatically:
- Detects system architecture
- Downloads static FFmpeg binary
- Installs Python dependencies
- Starts Gunicorn worker

**No manual configuration needed!**

---

## 🔒 Security & Privacy

### URL Validation
- Only accepts direct Spotify track URLs
- Rejects playlists, albums, artists
- Regexp-based URL validation

### File Management
- Downloaded files stored in system `/tmp`
- **Automatic cleanup** after download using `@after_this_request`
- Zero residual storage on server
- Ideal for Render's ephemeral disk

### Data Privacy
- No user tracking
- No analytics collection
- No file archival
- No metadata storage
- Stateless requests

---

## ⚙️ Environment Variables

```bash
PORT=5000                   # Server port (Render provides dynamically)
PYTHONUNBUFFERED=1         # Streaming logs (required)
```

---

## 🆘 Troubleshooting

### "FFmpeg not found"
```bash
# Auto-downloaded during build.sh
# Or manually:
bash build.sh
```

### "Invalid Spotify URL"
- Ensure: `https://open.spotify.com/track/[ID]`
- NOT: Playlists, albums, or shortened URLs
- To get correct URL: Spotify → Song → Share → Copy link

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

### "Download timeout"
- Max 5 minutes per track
- Try with a different song
- Check internet connection

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for 30+ solutions.

---

## 📊 Performance Specifications

| Metric | Value |
|--------|-------|
| **Concurrent Requests** | 4 (2 workers × 2 threads) |
| **Download Timeout** | 300 seconds (5 min) |
| **Max Assembly Time** | ~30-60 seconds per track |
| **Storage** | Ephemeral (/tmp) |
| **Cleanup** | Guaranteed per request |

---

## 📖 Additional Documentation

| File | Content |
|------|---------|
| **REFACTORING.md** | Technical refactoring details (v2.0) |
| **DEPLOY.md** | Step-by-step deployment guide |
| **TROUBLESHOOTING.md** | 30+ common issues & solutions |

---

## 🎵 Workflow Example: Using with Moises

### Step 1: Download with Pugify
1. Find track on Spotify: *"Bohemian Rhapsody" - Queen*
2. Share → Copy link
3. Paste into Pugify → Click Download
4. Get `bohemian_rhapsody.mp3`

### Step 2: Import to Moises
1. Upload `bohemian_rhapsody.mp3` to Moises
2. Wait for AI stem separation (~1-2 min)
3. Got separated tracks:
   - 🎙️ `vocals.mp3` (lead & harmonies)
   - 🥁 `drums.mp3`
   - 🎸 `other_instruments.mp3`
   - 🎼 `background.mp3`

### Step 3: Create Backing Track
1. Mute vocals in Moises
2. Combine drums + bass + instruments
3. Download mix as backing track
4. Practice with custom arrangement! 🎸

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.0** | Mar 31, 2026 | Render native + Gunicorn + FFmpeg static + rigorous cleanup |
| **1.0** | Mar 31, 2026 | Initial release |

---

## 📞 Support & References

- **Moises**: https://moises.ai
- **Spotify API Docs**: https://developer.spotify.com/documentation/web-api
- **Render Docs**: https://render.com/docs
- **Gunicorn**: https://gunicorn.org
- **FFmpeg**: https://ffmpeg.org

---

## ⚖️ Legal & Terms

### Personal Use Only
Pugify is strictly for personal, non-commercial music production use. 

### Spotify Terms
- Respect Spotify's Terms of Service
- Use downloaded music for personal practice only
- Do not distribute or commercially exploit downloads
- This tool does NOT bypass DRM - it works with Spotify's public APIs

### Music Copyright
All music remains copyrighted to original artists & rights holders. Downloaded files are for personal non-commercial use only.

---

## 🎯 Future Enhancements (Optional)

- [ ] Playlist batch downloading
- [ ] Multiple audio format support (M4A, OPUS, FLAC)
- [ ] Download history for repeat tracks
- [ ] Direct Moises integration (API export)
- [ ] Audio quality selection (128–320 kbps)
- [ ] Custom filename templates

---

## 🙏 Acknowledgments

- **spotdl**: Spotify track downloader library
- **yt-dlp**: Audio extraction engine
- **FFmpeg**: Audio codec & transcoding
- **Flask**: Python web framework
- **Gunicorn**: WSGI application server
- **Moises**: Inspiration for audio production workflow

---

## 📝 License

This project is **personal use software**. 

- ✅ Use for personal music production
- ✅ Fork for your own music practice
- ❌ Commercial redistribution
- ❌ Bypass DRM protections
- ❌ Violate Spotify Terms of Service

---

**Pugify** — *Empowering musicians to practice with purpose* 🎵

*Built for serious music learners who want to separate, analyze, and master individual tracks.*

---

*Created: March 31, 2026*  
*Purpose: Personal Music Production Utility*  
*Status: Production-Ready for Render*
