# 🎞️ GIF Creator

A web application that lets users upload images and create custom animated GIFs with adjustable speed and loop settings.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 📤 **Easy Upload** - Drag & drop or browse to select images
- 🖼️ **Live Preview** - See thumbnails of selected images before creating GIF
- ⚙️ **Customizable Settings** - Adjust frame duration and loop count
- 🎨 **Modern UI** - Clean, responsive interface with smooth animations
- ⚡ **Instant Results** - Generate and download GIFs in seconds
- 🌐 **Multiple Formats** - Supports PNG, JPG, JPEG, GIF, and WEBP

## 🚀 Live Demo

https://gif-creator-m3oe.onrender.com

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/sr-0521/GIF_creator.git
cd GIF_creator
```

2. **Create a virtual environment**
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## 📦 Dependencies

- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- imageio - Image processing and GIF creation
- gunicorn - Production server
- Pillow - Image manipulation

## 🎯 Usage

1. Click the upload area or drag images into it
2. Select 2 or more images from your computer
3. Adjust the frame duration (how long each image displays)
4. Set loop count (0 = infinite loop)
5. Click "Create GIF"
6. Preview your GIF and download it!

## 🌐 Deployment

This app is deployed on Render. To deploy your own instance:

1. Fork this repository
2. Sign up at [Render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Deploy!

## 📁 Project Structure

```
GIF_creator/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Saad Rizvi**
- GitHub: [@sr-0521](https://github.com/sr-0521)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- GIF creation powered by [imageio](https://imageio.readthedocs.io/)
- Deployed on [Render](https://render.com)

---

⭐ Star this repository if you find it helpful!
