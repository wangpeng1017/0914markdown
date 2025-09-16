from http.server import BaseHTTPRequestHandler
import tempfile
import os
import json
import re
from urllib.parse import unquote
import base64

# Try to import markitdown with minimal dependencies
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False
    print("MarkItDown not available, using fallback mode")

# Optimized document converter for Vercel deployment
class OptimizedConverter:
    def convert(self, file_path, filename):
        """Convert file to markdown with optimized dependencies"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            # Get file extension
            _, ext = os.path.splitext(filename.lower())
            
            # Try markitdown first if available
            if MARKITDOWN_AVAILABLE:
                try:
                    # Use markitdown for supported formats
                    if ext in ['.pdf', '.docx', '.xlsx']:
                        markitdown = MarkItDown()
                        result = markitdown.convert(file_path)
                        
                        # Add filename as title if not already present
                        content = result.text_content
                        if not content.startswith('#'):
                            content = f"# {filename}\n\n{content}"
                        
                        return Result(content)
                    else:
                        # Use fallback for other formats
                        return self._fallback_convert(file_path, filename, ext)
                        
                except Exception as e:
                    print(f"MarkItDown failed for {filename}: {str(e)}")
                    return self._fallback_convert(file_path, filename, ext)
            else:
                # Use fallback mode
                return self._fallback_convert(file_path, filename, ext)
                    
        except Exception as e:
            return Result(f"# Conversion Error\n\nFailed to convert {filename}: {str(e)}")
    
    def _fallback_convert(self, file_path, filename, ext):
        """Fallback conversion for basic formats when full markitdown is unavailable"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        if ext == '.txt':
            return self._convert_txt(file_path, filename)
        elif ext in ['.html', '.htm']:
            return self._convert_html(file_path, filename)
        elif ext in ['.csv']:
            return self._convert_csv(file_path, filename)
        else:
            # For unsupported formats in fallback mode
            supported_formats = ['.pdf', '.docx', '.xlsx']
            if ext in supported_formats:
                return Result(f"# {filename}\n\n## 转换失败\n\n此文件格式 **{ext.upper()}** 需要markitdown库支持，但当前不可用。\n\n### 支持的格式\n- PDF文档 (.pdf)\n- Word文档 (.docx)\n- Excel文件 (.xlsx)\n- HTML文件 (.html)\n- 文本文件 (.txt)\n- CSV文件 (.csv)\n\n### 当前状态\nMarkItDown库: {'✅ 可用' if MARKITDOWN_AVAILABLE else '❌ 不可用'}")
            else:
                return self._convert_unknown(file_path, filename, ext)
    
    def _convert_txt(self, file_path, filename):
        """Convert TXT files"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            # Try multiple encodings
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                        content = f.read()
                        return Result(f"# {filename}\n\n{content}")
                except UnicodeDecodeError:
                    continue
            
            return Result(f"# {filename}\n\n## 编码错误\n\n无法读取文件，尝试的编码：{', '.join(encodings)}")
            
        except Exception as e:
            return Result(f"# {filename}\n\n## 错误\n\n处理TXT文件时发生错误：{str(e)}")
    
    def _convert_unknown(self, file_path, filename, ext):
        """Handle unknown file formats"""
        class Result:
            def __init__(self, text):
                self.text_content = text
        
        try:
            # Try to detect if it's a text file
            with open(file_path, 'rb') as f:
                sample = f.read(1024)
            
            # Check if it's likely a text file (no null bytes in first 1KB)
            if b'\x00' in sample:
                return Result(f"# {filename}\n\n## 二进制文件\n\n检测到这是一个二进制文件 ({ext.upper()})，无法作为文本处理。\n\n### 支持的格式\n- PDF文档 (.pdf)\n- Word文档 (.docx)\n- Excel文件 (.xlsx)\n- HTML文件 (.html, .htm)\n- 文本文件 (.txt)\n- CSV文件 (.csv)\n\n### 当前状态\nMarkItDown库: {'✅ 可用' if MARKITDOWN_AVAILABLE else '❌ 不可用'}")
            
            # Try to read as text with multiple encoding attempts
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
            content = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                        content = f.read()[:5000]  # Limit to first 5000 chars
                        used_encoding = encoding
                        break
                except UnicodeDecodeError:
                    continue
            
            if content is not None:
                return Result(f"# {filename}\n\n*检测编码: {used_encoding}*\n\n```\n{content}\n```\n\n---\n*注意：此文件被当作文本处理，可能不是最佳转换方式。*")
            else:
                return Result(f"# {filename}\n\n## 编码错误\n\n无法使用常见编码方式读取此文件。\n\n尝试的编码：{', '.join(encodings)}\n\n请确保文件是有效的文本格式。")
                
        except Exception as e:
            return Result(f"# {filename}\n\n## 处理错误\n\n处理文件时发生错误：{str(e)}")
    
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
                # Convert file using optimized converter
                converter = OptimizedConverter()
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