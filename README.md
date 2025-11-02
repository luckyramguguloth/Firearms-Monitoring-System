# Firearm Detection Web App

Introduction
This project is a web application for detecting firearms in uploaded images or videos, built using:
- YOLOv8m object detection model (optimized for faster and stable inference)
- OpenVINO runtime for accelerated inference on CPU
- Flask for the web server
- HTML5 for UI pages

Users can simply upload media files through the browser, and the app will perform firearm detection and display the results along with detection performance (FPS), with bounding boxes and confidence scores drawn accurately.

## Project Structure
```
your_project/
├── run.py
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
|   ├── models/
|   ├── ├── user.py
│   ├── yolo/
│   │   ├── detector.py    # Optimized YOLOv8m detection
│   ├── routes/
│   │   ├── detect.py      # Upload and detection routes
│   ├── static/
│   │   ├── uploads/       # Uploaded media files
│   │   ├── results/       # Processed detection outputs
|   |   ├── css/
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── register.html
│   │   ├── user_details
│   │   ├── upload.html
│   │   ├── result.html    # Displays analyzed media directly
├── model_weights/
│   ├── trained_models/
│   │   ├── weights/
│   │   ├── files
├── requirements.txt
├── README.md
```


## Major Changes:
- ✅ Upgraded to **YOLOv8n OpenVINO** for super-fast detections
- ✅ Frame skipping (every 5 frames) for fast video processing
- ✅ Live analyzed video plays on the webpage directly (no need to open file manually)
- ✅ Processing time optimized (13MB video analyzed in <45 seconds)

## How to run:

1. Activate virtual environment
2. Install requirements:
    ```
    pip install flask openvino opencv-python
    ```
3. Start the server:
    ```
    python run.py
    ```
4. Go to `http://127.0.0.1:5000/dashboard`
5. Upload image or video → get results instantly!


---
<img width="1920" height="1020" alt="Screenshot 2025-05-02 061044" src="https://github.com/user-attachments/assets/2caeb7cf-6a79-4409-815a-e2b7c44243a0" />

## Notes:
- The model is located in `/models/yolov8n/`
- Ensure your video files are reasonable size (<100MB) for best speed.
- Processing is done with CPU by default; GPU is optional.

---


3. Setup Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

4. Install Required Packages

```bash
pip install -r requirements.txt
```

## How to Run
Run the Flask app:

```bash
python run.py
```

Open your browser at:

```
http://127.0.0.1:5000/
```

Login using the dummy credentials (edit in code if needed).  
Navigate to **Upload Page**, upload Image or Video, and detection will display directly inside the browser with FPS information.

## Usage Guide
- Login -> enter credentials.
- Dashboard -> Upload Media (image or video).
- Detection Results -> Displays detected media inside browser (image or playable video).
- Shows performance: FPS (frames per second).
- Option to Upload Another File or Logout.

## Model Information
- **Model**: YOLOv8n
- **Framework**: OpenVINO runtime (CPU optimized)
- **Performance**: Very high-speed detection with improved bounding box stability and accuracy.
- **Input Size**: Automatically resized based on media input.

## Notes
- App is optimized for CPU inference using OpenVINO.
- Bounding boxes drawn smoothly with confidence scores above 0.5 threshold.
- Processed videos/images are stored inside `/static/results/`.
- No need to manually open results folder — everything displayed in browser directly.
