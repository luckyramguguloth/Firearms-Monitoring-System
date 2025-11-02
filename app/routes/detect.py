import os
from flask import Blueprint, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from app.yolo.detector import run_detection
from urllib.parse import unquote
from app.models.user import Prediction, db
from flask_login import current_user


detect_bp = Blueprint("detect", __name__)

UPLOAD_FOLDER = r"C:\Users\laxma\Desktop\projects\myprojects\FIREARMS_FOR_MAJOR\FILES2\app\static\uploads"
RESULT_FOLDER = r"C:\Users\laxma\Desktop\projects\myprojects\FIREARMS_FOR_MAJOR\FILES2\app\static\results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@detect_bp.route("/", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, filename)

            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in [".mp4", ".avi", ".mov"]:
                result_name = os.path.splitext(filename)[0] + "_resultvideo.mp4"
            else:
                result_name = os.path.splitext(filename)[0] + "_resultimage.jpg"

            result_path = os.path.join(RESULT_FOLDER, result_name)
            file.save(upload_path)

            result_file = run_detection(upload_path, RESULT_FOLDER)
            result_file_web = os.path.basename(result_file)  # Only the filename

            if result_file.lower().endswith((".mp4", ".avi", ".mov")):
                return render_template("result.html", result_video=result_file_web)
            else:
                return render_template("result.html", result_image=result_file_web)

    return render_template("upload.html")

@detect_bp.route("/download/<path:filename>")
def download_file(filename):
    safe_filename = os.path.basename(unquote(filename))
    return send_from_directory(RESULT_FOLDER, safe_filename, as_attachment=True)

