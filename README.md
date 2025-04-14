# Apple Classifier App

This is a web application that classifies apples in images based on their color (Red, Yellow, Green). The app uses deep learning via Roboflow for apple detection and classification and is built with FastAPI for the backend and HTML/JavaScript for the frontend.

## Features
- **Apple Detection**: Detects apples in uploaded images using a pre-trained Roboflow model.
- **Apple Classification by Color**: Classifies each detected apple as Red, Yellow, or Green using pixel color analysis.
- **Image Cropping**: Crops each detected apple from the original image and saves it into separate directories by color.
- **Frontend Display**: Displays cropped apples with labels on the web interface after upload.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Model**: Roboflow (for apple detection)
- **Libraries/Tools**:
  - `requests`: Communicating with Roboflow API
  - `Pillow`: Image cropping and saving
  - `OpenCV`: Image processing (optional)
  - `NumPy`: Color classification
  - `Uvicorn`: ASGI server for FastAPI

## Requirements

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/apple_classifier_app.git
cd apple_classifier_app
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add:

```
ROBOFLOW_API_KEY=your_roboflow_api_key
ROBOFLOW_MODEL_ID=apple-detection_0630/6
```

Alternatively, you can hardcode these values in `detect.py` if preferred (not recommended for production).

### 5. Running the App
```bash
uvicorn app.main:app --reload
```

Then open your browser and navigate to:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. How to Use
- Upload an image with apples.
- The backend detects and crops apples.
- Each cropped apple is classified by color.
- Cropped apples appear on the page, grouped by color.

## Folder Structure

```
apple_classifier_app/
├── app/
│   ├── main.py            # FastAPI routes
│   ├── detect.py          # Apple detection & classification logic
│   ├── static/
│   │   ├── uploads/       # Original uploaded images
│   │   └── crops/
│   │       ├── red/       # Red apples
│   │       ├── green/     # Green apples
│   │       └── yellow/    # Yellow apples
│   ├── templates/
│   │   └── index.html     # Frontend page
│   └── script.js          # Handles upload and dynamic result rendering
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## Demo

🎥 Watch the demo here: [Google Drive Demo Video](https://drive.google.com/file/d/19Pf7F6G4g97N-JogDjM3bl2x2ID2eyYf/view?usp=sharing)

## Contributions

Feel free to fork this repository and submit pull requests. Open issues for bugs or feature requests!

## License

This project is licensed under the MIT License.
