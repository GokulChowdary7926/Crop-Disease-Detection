# 🌱 Crop Disease Detection System

## Project Overview
The **Crop Disease Detection System** is an AI-powered web application that identifies plant diseases from images using advanced deep learning. Built with YOLOv8 object detection model, it provides real-time disease detection, comprehensive disease information, prevention methods, and treatment recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22+-red.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-8.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🖼️ Image Upload**: Easy drag-and-drop interface for uploading plant images
- **🔍 Real-time Disease Detection**: AI-powered detection using YOLOv8 model
- **📚 Comprehensive Information**: Detailed disease descriptions from Wikipedia
- **🛡️ Prevention & Treatment**: Expert recommendations and guidelines
- **🛒 Product Recommendations**: Links to treatment products (with API keys)
- **💻 Modern Web Interface**: Beautiful, responsive UI with professional design
- **📊 Detection Metrics**: Confidence scores and detailed analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GokulChowdary7926/Crop-Disease-Detection.git
   cd Crop-Disease-Detection
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run crop.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📋 Requirements

- streamlit==1.22.0
- ultralytics==8.0.0
- Pillow==10.0.1
- requests==2.31.0
- numpy==1.26.0
- wikipedia==1.4.0

## 🎯 Usage Guide

1. **Upload Image**: Click on the upload area and select a clear image of the plant leaf or affected area
2. **Wait for Analysis**: The AI model will analyze the image in real-time
3. **View Results**: See detected diseases with confidence scores
4. **Get Information**: Access detailed disease information, prevention methods, and treatment recommendations

### Tips for Best Results:
- Use clear, well-lit images
- Focus on the affected area
- Ensure good image quality (minimum 500x500 pixels)
- Take photos in natural light when possible

## 🤖 Model Information

### Architecture
- **Model**: YOLOv8 (You Only Look Once version 8)
- **Input Size**: 640x640 pixels
- **Framework**: PyTorch
- **Library**: Ultralytics

### Training Details
- **Dataset**: Custom plant disease dataset
- **Batch Size**: 16
- **Learning Rate**: 0.001
- **Epochs**: 50
- **Optimizer**: Adam

### Model File
The trained model is located at `model/last (2).pt`

## 🔧 Configuration

### Optional: Google Custom Search API
To enable web-based prevention information and product recommendations:

1. Get a Google Custom Search API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create a Custom Search Engine at [Google Programmable Search](https://programmablesearchengine.google.com/)
3. Update the API keys in `crop.py` (lines 9-10):
   ```python
   API_KEY = 'your_google_api_key'
   SEARCH_ENGINE_ID = 'your_custom_search_engine_id'
   ```

**Note**: The application works perfectly without API keys, providing general prevention advice and Wikipedia information.

## 📁 Project Structure

```
Crop-Disease-Detection/
│
├── crop.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── model/
│   ├── last (2).pt       # Trained YOLOv8 model
│   └── model_docs.md     # Model documentation
│
└── Assets/                # Training assets and demo
    ├── demo.mp4
    ├── confusion_matrix.png
    └── ...
```

## 🎨 UI Features

- **Modern Design**: Professional gradient-based UI with smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Real-time Detection**: Instant results with visual bounding boxes
- **Tabbed Interface**: Organized information display
- **Interactive Elements**: Hover effects and smooth transitions

## 📊 Performance

- Real-time detection (< 2 seconds per image)
- High accuracy disease classification
- Support for multiple disease types
- Confidence score visualization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/yolov8) for the object detection model
- [Streamlit](https://streamlit.io/) for the web framework
- [Wikipedia API](https://www.mediawiki.org/wiki/API) for disease information
- All contributors and the open-source community

## 📧 Contact

For questions, feedback, or contributions:
- **GitHub Issues**: [Create an issue](https://github.com/GokulChowdary7926/Crop-Disease-Detection/issues)
- **Repository**: [Crop-Disease-Detection](https://github.com/GokulChowdary7926/Crop-Disease-Detection)

## 🌟 Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ using AI and Deep Learning**
