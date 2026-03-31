# Gunicorn configuration for Render deployment
import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes
workers = max(2, multiprocessing.cpu_count() - 1)
worker_class = "gthread"
threads = 2
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Application
raw_env = [
    "PYTHONUNBUFFERED=1",
]

# Server hooks
def post_worker_init(worker):
    """Called just before a worker is forked to work on the WSGI application."""
    pass
