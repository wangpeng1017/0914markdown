from http.server import BaseHTTPRequestHandler
import tempfile
import os
import io
import json
from urllib.parse import parse_qs, urlparse

try:
    from markitdown import MarkItDown
except ImportError:
    # Fallback for development
    class MarkItDown:
        def convert(self, file_path):
            class Result:
                def __init__(self, text):
                    self.text_content = text
            return Result(f"# Conversion Error\n\nMarkItDown library not available. Original file: {file_path}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse content type and boundary
            content_type = self.headers.get('content-type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Only multipart/form-data is supported")
                return

            # Get content length
            content_length = int(self.headers.get('content-length', 0))
            if content_length == 0:
                self.send_error(400, "No file data received")
                return

            # Read the form data
            form_data = self.rfile.read(content_length)
            
            # Simple multipart parsing (for basic file upload)
            boundary = content_type.split('boundary=')[1].encode()
            parts = form_data.split(b'--' + boundary)
            
            file_data = None
            filename = None
            
            for part in parts:
                if b'filename=' in part and b'Content-Type:' in part:
                    # Extract filename
                    lines = part.split(b'\r\n')
                    for line in lines:
                        if b'filename=' in line:
                            filename = line.decode().split('filename="')[1].split('"')[0]
                            break
                    
                    # Extract file content (after double CRLF)
                    content_start = part.find(b'\r\n\r\n')
                    if content_start != -1:
                        file_data = part[content_start + 4:]
                        # Remove trailing CRLF
                        if file_data.endswith(b'\r\n'):
                            file_data = file_data[:-2]
                    break
            
            if not file_data or not filename:
                self.send_error(400, "No valid file found in request")
                return

            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(file_data)
                temp_path = temp_file.name

            try:
                # Convert file using MarkItDown
                md = MarkItDown()
                result = md.convert(temp_path)
                markdown_content = result.text_content
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                response = {
                    'success': True,
                    'markdown': markdown_content,
                    'filename': os.path.splitext(filename)[0] + '.md'
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                # Send error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': False,
                    'error': f'Conversion failed: {str(e)}'
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
            
            self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()