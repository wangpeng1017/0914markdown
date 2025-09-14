from http.server import BaseHTTPRequestHandler
import tempfile
import os
import json
import re
from urllib.parse import unquote
import base64

# Lightweight document converter without heavy dependencies
class LightweightConverter:
    def convert(self, file_path, filename):
        """Convert file to markdown using built-in Python libraries"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            # Get file extension
            _, ext = os.path.splitext(filename.lower())
            
            if ext == '.txt':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return Result(f"# {filename}\n\n{content}")
            
            elif ext in ['.html', '.htm']:
                return self._convert_html(file_path, filename)
            
            elif ext in ['.csv']:
                return self._convert_csv(file_path, filename)
                
            else:
                # For unsupported formats, try to read as text
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:5000]  # Limit to first 5000 chars
                        return Result(f"# {filename}\n\n```\n{content}\n```\n\n*Note: This file format is not fully supported in the lightweight version. For full support of PDF, Word, Excel, and PowerPoint files, please use a local installation with the full markitdown library.*")
                except:
                    return Result(f"# {filename}\n\n*This file format is not supported in the lightweight version. For full support of PDF, Word, Excel, and PowerPoint files, please use a local installation with the full markitdown library.*")
                    
        except Exception as e:
            return Result(f"# Conversion Error\n\nFailed to convert {filename}: {str(e)}")
    
    def _convert_html(self, file_path, filename):
        """Simple HTML to Markdown conversion"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Simple HTML to Markdown conversion
            markdown = self._html_to_markdown(html_content)
            return Result(f"# {filename}\n\n{markdown}")
        except Exception as e:
            return Result(f"# Conversion Error\n\nFailed to convert HTML: {str(e)}")
    
    def _html_to_markdown(self, html):
        """Basic HTML to Markdown conversion"""
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert headers
        html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.IGNORECASE)
        html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.IGNORECASE)
        html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.IGNORECASE)
        html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.IGNORECASE)
        
        # Convert paragraphs
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert line breaks
        html = re.sub(r'<br[^>]*>', '\n', html, flags=re.IGNORECASE)
        
        # Convert bold and italic
        html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.IGNORECASE)
        html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.IGNORECASE)
        html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.IGNORECASE)
        html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.IGNORECASE)
        
        # Convert links
        html = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
        html = html.strip()
        
        return html
    
    def _convert_csv(self, file_path, filename):
        """Convert CSV to Markdown table"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:100]  # Limit to first 100 rows
            
            if not lines:
                return Result(f"# {filename}\n\nEmpty CSV file")
            
            markdown = f"# {filename}\n\n"
            
            # Simple CSV parsing (basic, doesn't handle complex cases)
            rows = []
            for line in lines:
                row = [cell.strip('"').strip() for cell in line.strip().split(',')]
                rows.append(row)
            
            if rows:
                # Header row
                header = rows[0]
                markdown += "| " + " | ".join(header) + " |\n"
                markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
                
                # Data rows
                for row in rows[1:]:
                    # Ensure row has same number of columns as header
                    while len(row) < len(header):
                        row.append("")
                    markdown += "| " + " | ".join(row[:len(header)]) + " |\n"
            
            return Result(markdown)
        except Exception as e:
            return Result(f"# Conversion Error\n\nFailed to convert CSV: {str(e)}")

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
                # Convert file using lightweight converter
                converter = LightweightConverter()
                result = converter.convert(temp_path, filename)
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