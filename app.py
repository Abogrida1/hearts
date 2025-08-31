import os
from flask import Flask, render_template, request, jsonify, send_file
import requests
import tempfile
import re
import logging
import json
import threading
import yt_dlp
from urllib.parse import urlparse, parse_qs
from pathlib import Path

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

    # Enable CORS manually
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    # Serve CSS file directly
    @app.route('/style.css')
    def serve_css():
        return app.send_static_file('style.css')

    # Configure logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)

    return app

app = create_app()

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    parsed_url = urlparse(url)
    
    if 'youtube.com' in parsed_url.netloc:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path[1:]
    
    return None

def get_video_info(video_id):
    """Get video information using yt-dlp"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'author': info.get('uploader', 'Unknown Author'),
                'author_url': info.get('uploader_url', ''),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'formats': info.get('formats', [])
            }
    except Exception as e:
        app.logger.error(f"Error getting video info: {e}")
    
    return None

def get_download_links(video_id):
    """Generate download links for different qualities using yt-dlp"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            
            # Add audio format (best audio)
            audio_formats = [f for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            if audio_formats:
                best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) if x.get('abr') else 0)
                formats.append({
                    'format_id': 'audio',
                    'ext': 'mp3',
                    'quality': f"Audio {best_audio.get('abr', 'Unknown')}kbps",
                    'filesize': f"~{best_audio.get('filesize', 0) // (1024*1024) if best_audio.get('filesize') else 'Unknown'}MB",
                    'type': 'audio',
                    'url': url,
                    'note': 'Direct MP3 download from our server',
                    'format_info': best_audio
                })
            
            # Add video formats
            video_formats = [f for f in info.get('formats', []) if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            
            # Find 720p format
            hd_formats = [f for f in video_formats if f.get('height') == 720]
            if hd_formats:
                best_hd = max(hd_formats, key=lambda x: x.get('filesize', 0) if x.get('filesize') else 0)
                formats.append({
                    'format_id': '720p',
                    'ext': 'mp4',
                    'quality': '720p HD',
                    'filesize': f"~{best_hd.get('filesize', 0) // (1024*1024) if best_hd.get('filesize') else 'Unknown'}MB",
                    'type': 'video',
                    'url': url,
                    'note': 'Direct download from our server',
                    'format_info': best_hd
                })
            
            # Find 480p format
            sd_formats = [f for f in video_formats if f.get('height') == 480]
            if sd_formats:
                best_sd = max(sd_formats, key=lambda x: x.get('filesize', 0) if x.get('filesize') else 0)
                formats.append({
                    'format_id': '480p',
                    'ext': 'mp4',
                    'quality': '480p HD',
                    'filesize': f"~{best_sd.get('filesize', 0) // (1024*1024) if best_sd.get('filesize') else 'Unknown'}MB",
                    'type': 'video',
                    'url': url,
                    'note': 'Direct download from our server',
                    'format_info': best_sd
                })
            
            # If no specific formats found, add best available
            if not formats:
                best_format = max(video_formats, key=lambda x: x.get('height', 0) if x.get('height') else 0)
                formats.append({
                    'format_id': 'best',
                    'ext': 'mp4',
                    'quality': f"{best_format.get('height', 'Unknown')}p",
                    'filesize': f"~{best_format.get('filesize', 0) // (1024*1024) if best_format.get('filesize') else 'Unknown'}MB",
                    'type': 'video',
                    'url': url,
                    'note': 'Best available quality',
                    'format_info': best_format
                })
            
            return formats
            
    except Exception as e:
        app.logger.error(f"Error getting download links: {e}")
        # Fallback to basic formats
        return [
            {
                'format_id': '720p',
                'ext': 'mp4',
                'quality': '720p HD',
                'filesize': '~50MB',
                'type': 'video',
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'note': 'Direct download from our server'
            },
            {
                'format_id': '480p',
                'ext': 'mp4',
                'quality': '480p SD',
                'filesize': '30MB',
                'type': 'video',
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'note': 'Direct download from our server'
            },
            {
                'format_id': 'audio',
                'ext': 'mp3',
                'quality': 'Audio Only (MP3)',
                'filesize': '5MB',
                'type': 'audio',
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'note': 'Direct MP3 download from our server'
            }
        ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL مطلوب'}), 400
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({'error': 'رابط YouTube غير صحيح'}), 400
        
        # Get video information
        video_info = get_video_info(video_id)
        if not video_info:
            return jsonify({'error': 'لا يمكن جلب معلومات الفيديو'}), 500
        
        # Get download formats
        formats = get_download_links(video_id)
        
        return jsonify({
            'title': video_info['title'],
            'thumbnail': video_info['thumbnail'],
            'author': video_info['author'],
            'video_id': video_id,
            'duration': video_info.get('duration', 0),
            'view_count': video_info.get('view_count', 0),
            'formats': formats
        })
        
    except Exception as e:
        app.logger.error(f"Error in get_info: {e}")
        return jsonify({'error': f'خطأ في جلب المعلومات: {str(e)}'}), 500

@app.route('/download_direct/<video_id>/<format_type>')
def download_direct(video_id, format_type):
    """Direct download with actual file using yt-dlp"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create temporary directory for downloads
        temp_dir = Path(tempfile.gettempdir()) / "youtube_downloads"
        temp_dir.mkdir(exist_ok=True)
        
        # Get video info for filename
        video_info = get_video_info(video_id)
        if not video_info:
            return jsonify({'error': 'لا يمكن جلب معلومات الفيديو'}), 500
        
        # Create safe filename
        safe_title = "".join(c for c in video_info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50]  # Limit length
        
        if format_type == 'audio':
            filename = f"{safe_title}.mp3"
            content_type = 'audio/mpeg'
            # Download audio only
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(temp_dir / filename),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
        else:
            # Download video with specific quality
            if format_type == '720p':
                format_spec = 'best[height<=720]/best'
            elif format_type == '480p':
                format_spec = 'best[height<=480]/best'
            else:
                format_spec = 'best'
            
            filename = f"{safe_title}_{format_type}.mp4"
            content_type = 'video/mp4'
            
            ydl_opts = {
                'format': format_spec,
                'outtmpl': str(temp_dir / filename),
                'quiet': True,
                'no_warnings': True,
            }
        
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if file was downloaded
        file_path = temp_dir / filename
        if not file_path.exists():
            return jsonify({'error': 'فشل في تحميل الملف'}), 500
        
        # Return the actual file for download
        return send_file(
            file_path,
            mimetype=content_type,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        app.logger.error(f"Error in download_direct: {e}")
        return jsonify({'error': f'خطأ في التحميل: {str(e)}'}), 500

@app.route('/download_buttons/<video_id>')
def download_buttons(video_id):
    """Get download buttons HTML for a video"""
    try:
        # Get video info
        video_info = get_video_info(video_id)
        if not video_info:
            return jsonify({'error': 'لا يمكن جلب معلومات الفيديو'}), 500
        
        # Create safe filename
        safe_title = "".join(c for c in video_info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50]  # Limit length
        
        # Generate download buttons HTML
        buttons_html = f"""
        <div class="download-buttons">
            <h3>تحميل {video_info['title']}</h3>
            <div class="button-group">
                <a href="/download_direct/{video_id}/audio" class="btn btn-audio" download="{safe_title}.mp3">
                    🎵 تحميل الصوت (MP3)
                </a>
                <a href="/download_direct/{video_id}/720p" class="btn btn-video" download="{safe_title}_720p.mp4">
                    🎬 تحميل الفيديو (720p)
                </a>
                <a href="/download_direct/{video_id}/480p" class="btn btn-video" download="{safe_title}_480p.mp4">
                    🎬 تحميل الفيديو (480p)
                </a>
            </div>
        </div>
        """
        
        return jsonify({
            'success': True,
            'buttons_html': buttons_html,
            'title': video_info['title']
        })
        
    except Exception as e:
        app.logger.error(f"Error in download_buttons: {e}")
        return jsonify({'error': f'خطأ في إنشاء أزرار التحميل: {str(e)}'}), 500

@app.route('/api/video/<video_id>')
def video_info(video_id):
    """Get video information by ID"""
    try:
        video_info = get_video_info(video_id)
        if video_info:
            return jsonify(video_info)
        else:
            return jsonify({'error': 'فيديو غير موجود'}), 404
    except Exception as e:
        app.logger.error(f"Error in video_info: {e}")
        return jsonify({'error': 'خطأ في جلب المعلومات'}), 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 Starting YouTube Downloader App on port {port}")
        print(f"📱 Open your browser: http://localhost:{port}")
        print("⏹️  Press Ctrl+C to stop")
        print("-" * 50)
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        input("Press Enter to exit...")

# For production servers (Render, Heroku, etc.)
app = app
