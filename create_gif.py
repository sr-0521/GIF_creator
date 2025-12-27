from flask import Flask, request, send_file, jsonify, render_template_string
from flask_cors import CORS
import imageio.v3 as iio
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GIF Creator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }

        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            background: #f8f9ff;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 30px;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f1ff;
        }

        .upload-area.dragover {
            border-color: #764ba2;
            background: #e8e9ff;
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }

        input[type="file"] {
            display: none;
        }

        .file-label {
            color: #667eea;
            font-weight: 600;
            font-size: 1.1em;
        }

        .preview-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
        }

        .preview-item {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            aspect-ratio: 1;
        }

        .preview-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .remove-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background: rgba(255, 59, 48, 0.9);
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.3s;
        }

        .remove-btn:hover {
            background: rgba(255, 59, 48, 1);
        }

        .controls {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .control-group {
            flex: 1;
            min-width: 200px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }

        input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }

        .button-group {
            display: flex;
            gap: 15px;
        }

        button {
            flex: 1;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .create-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .create-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }

        .create-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .clear-btn {
            background: #f0f0f0;
            color: #666;
        }

        .clear-btn:hover {
            background: #e0e0e0;
        }

        .result {
            text-align: center;
            margin-top: 30px;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
            display: none;
        }

        .result.show {
            display: block;
        }

        .result img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }

        .download-btn {
            background: #34c759;
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 10px;
            display: inline-block;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .download-btn:hover {
            background: #2db04d;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(52, 199, 89, 0.4);
        }

        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            font-weight: 600;
            margin: 20px 0;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .file-count {
            color: #667eea;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎞️ GIF Creator</h1>
        <p class="subtitle">Upload images and create your animated GIF</p>

        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <p class="file-label">Click to browse or drag & drop images here</p>
            <p style="color: #999; margin-top: 10px; font-size: 0.9em;">Supports PNG, JPG, JPEG, GIF, WEBP</p>
            <input type="file" id="fileInput" multiple accept="image/*">
        </div>

        <div class="file-count" id="fileCount" style="display: none;">
            <span id="fileCountText">0 images selected</span>
        </div>

        <div class="preview-container" id="previewContainer"></div>

        <div class="controls">
            <div class="control-group">
                <label for="duration">Frame Duration (ms)</label>
                <input type="number" id="duration" value="500" min="100" max="5000" step="100">
            </div>
            <div class="control-group">
                <label for="loop">Loop Count (0 = infinite)</label>
                <input type="number" id="loop" value="0" min="0" max="100">
            </div>
        </div>

        <div class="button-group">
            <button class="create-btn" id="createBtn" disabled>Create GIF</button>
            <button class="clear-btn" id="clearBtn">Clear All</button>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Creating your GIF...</p>
        </div>

        <div class="result" id="result">
            <h2 style="margin-bottom: 20px; color: #333;">Your GIF is ready! 🎉</h2>
            <img id="resultGif" src="" alt="Generated GIF">
            <br>
            <a href="#" class="download-btn" id="downloadBtn" download="animation.gif">Download GIF</a>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const previewContainer = document.getElementById('previewContainer');
        const createBtn = document.getElementById('createBtn');
        const clearBtn = document.getElementById('clearBtn');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const resultGif = document.getElementById('resultGif');
        const downloadBtn = document.getElementById('downloadBtn');
        const fileCount = document.getElementById('fileCount');
        const fileCountText = document.getElementById('fileCountText');

        uploadArea.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        function handleFiles(files) {
            for (let file of files) {
                if (file.type.startsWith('image/')) {
                    selectedFiles.push(file);
                    addPreview(file);
                }
            }
            updateUI();
        }

        function addPreview(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const div = document.createElement('div');
                div.className = 'preview-item';
                div.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <button class="remove-btn" onclick="removeFile('${file.name}')">×</button>
                `;
                previewContainer.appendChild(div);
            };
            reader.readAsDataURL(file);
        }

        function removeFile(filename) {
            selectedFiles = selectedFiles.filter(f => f.name !== filename);
            previewContainer.innerHTML = '';
            selectedFiles.forEach(file => addPreview(file));
            updateUI();
        }

        function updateUI() {
            createBtn.disabled = selectedFiles.length < 2;
            if (selectedFiles.length > 0) {
                fileCount.style.display = 'block';
                fileCountText.textContent = `${selectedFiles.length} image${selectedFiles.length > 1 ? 's' : ''} selected`;
            } else {
                fileCount.style.display = 'none';
            }
        }

        clearBtn.addEventListener('click', () => {
            selectedFiles = [];
            previewContainer.innerHTML = '';
            fileInput.value = '';
            result.classList.remove('show');
            updateUI();
        });

        createBtn.addEventListener('click', async () => {
            if (selectedFiles.length < 2) {
                alert('Please select at least 2 images');
                return;
            }

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('images', file);
            });
            formData.append('duration', document.getElementById('duration').value);
            formData.append('loop', document.getElementById('loop').value);

            loading.classList.add('show');
            result.classList.remove('show');
            createBtn.disabled = true;

            try {
                const response = await fetch('/create_gif', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    resultGif.src = url;
                    downloadBtn.href = url;
                    result.classList.add('show');
                } else {
                    alert('Error creating GIF. Please try again.');
                }
            } catch (error) {
                alert('Error creating GIF: ' + error.message);
            } finally {
                loading.classList.remove('show');
                createBtn.disabled = false;
            }
        });

        window.removeFile = removeFile;
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/create_gif', methods=['POST'])
def create_gif():
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400
    
    files = request.files.getlist('images')
    
    if len(files) < 2:
        return jsonify({'error': 'At least 2 images required'}), 400
    
    duration = int(request.form.get('duration', 500))
    loop = int(request.form.get('loop', 0))
    
    images = []
    temp_files = []
    
    try:
        # Save uploaded files temporarily and read them
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                temp_files.append(filepath)
                images.append(iio.imread(filepath))
        
        # Create GIF in memory
        gif_bytes = io.BytesIO()
        iio.imwrite(gif_bytes, images, extension='.gif', duration=duration, loop=loop)
        gif_bytes.seek(0)
        
        return send_file(gif_bytes, mimetype='image/gif', as_attachment=False, download_name='animation.gif')
    
    finally:
        # Clean up temporary files
        for filepath in temp_files:
            try:
                os.remove(filepath)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)