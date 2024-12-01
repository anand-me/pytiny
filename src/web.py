from flask import Flask, redirect, request, jsonify, abort
from urllib.parse import urlparse
from .core import PyTiny
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
shortener = PyTiny()

def is_valid_url(url):
    """Validate URL format and accessibility."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def generate_qr_code(url):
    """Generate QR code for a URL."""
    try:
        img_buffer = io.BytesIO()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"QR Code generation error: {str(e)}")
        return None

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyTiny URL Shortener</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8 max-w-2xl">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h1 class="text-2xl font-bold mb-6">URL Shortener</h1>
                
                <!-- Error Alert (hidden by default) -->
                <div id="errorAlert" class="hidden bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    <span id="errorMessage"></span>
                </div>

                <form id="urlForm" class="space-y-4">
                    <div>
                        <label class="block text-gray-700 mb-2">URL to Shorten</label>
                        <input type="url" id="url" name="url" required
                               class="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                               placeholder="https://example.com">
                    </div>
                    
                    <div>
                        <label class="block text-gray-700 mb-2">Expire After (hours)</label>
                        <input type="number" id="expire_hours" name="expire_hours"
                               class="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                               value="24" min="1">
                    </div>

                    <div class="flex items-center">
                        <input type="checkbox" id="generate_qr" name="generate_qr" class="mr-2">
                        <label for="generate_qr">Generate QR Code</label>
                    </div>

                    <button type="submit" 
                            class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                        Shorten URL
                    </button>
                </form>

                <!-- Results Section (hidden by default) -->
                <div id="results" class="hidden mt-6 pt-6 border-t">
                    <h2 class="text-xl font-bold mb-4">Your Shortened URL</h2>
                    <div class="bg-gray-50 p-4 rounded">
                        <div class="flex items-center space-x-2">
                            <input type="text" id="shortUrl" readonly
                                   class="flex-1 p-2 border rounded bg-white">
                            <button onclick="copyUrl()"
                                    class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                                Copy
                            </button>
                        </div>
                    </div>
                    <div id="qrCode" class="hidden mt-4 text-center">
                        <h3 class="text-lg font-bold mb-2">QR Code</h3>
                        <img id="qrCodeImage" class="mx-auto">
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('urlForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Hide previous error and results
                document.getElementById('errorAlert').classList.add('hidden');
                document.getElementById('results').classList.add('hidden');
                
                const formData = new FormData(e.target);
                
                try {
                    const response = await fetch('/shorten', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.error || 'Failed to shorten URL');
                    }
                    
                    // Show results
                    document.getElementById('results').classList.remove('hidden');
                    document.getElementById('shortUrl').value = data.short_url;
                    
                    // Handle QR code if present
                    if (data.qr_code) {
                        document.getElementById('qrCode').classList.remove('hidden');
                        document.getElementById('qrCodeImage').src = data.qr_code;
                    } else {
                        document.getElementById('qrCode').classList.add('hidden');
                    }
                    
                } catch (error) {
                    const errorDiv = document.getElementById('errorAlert');
                    const errorMessage = document.getElementById('errorMessage');
                    errorMessage.textContent = error.message;
                    errorDiv.classList.remove('hidden');
                }
            });

            function copyUrl() {
                const urlInput = document.getElementById('shortUrl');
                urlInput.select();
                document.execCommand('copy');
                alert('URL copied to clipboard!');
            }
        </script>
    </body>
    </html>
    '''

@app.route('/shorten', methods=['POST'])
def shorten():
    """Handle URL shortening requests."""
    try:
        url = request.form.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400

        expire_hours = request.form.get('expire_hours')
        try:
            expire_hours = int(expire_hours) if expire_hours else 24
        except ValueError:
            return jsonify({'error': 'Invalid expiration hours'}), 400

        generate_qr = request.form.get('generate_qr') == 'on'

        # Create short URL
        code = shortener.create_short_url(url, expire_hours=expire_hours)
        short_url = f"{request.host_url}{code}"

        response_data = {
            'short_url': short_url,
            'stats': shortener.get_stats(code)
        }

        if generate_qr:
            qr_code = generate_qr_code(short_url)
            if qr_code:
                response_data['qr_code'] = qr_code

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/<short_code>')
def redirect_url(short_code):
    """Handle URL redirection."""
    try:
        long_url = shortener.get_long_url(short_code)
        if long_url:
            return redirect(long_url)
        return "URL not found or expired", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)