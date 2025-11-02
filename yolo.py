from ultralytics import YOLO

def download_model():
    print("Downloading YOLOv8 base model (yolov8n.pt)...")
    model = YOLO('yolov8n.pt')  # This will download yolov8s if not present
    print("Model downloaded and ready.")

if __name__ == "__main__":
    download_model()
