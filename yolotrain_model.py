import os
from datetime import datetime
from ultralytics import YOLO

# === CONFIGURATION ===
yaml_file = r"C:\Users\laxma\Desktop\projects\myprojects\FIREARMS_FOR_MAJOR\FILES2\Separated\dataset_prepared\data.yaml"  # Replace with actual YAML path
base_model = "yolov8n.pt"        # Smallest, lightest base model

# === TRAINING LIMITS ===
epochs = 10
imgsz = 416
batch = 4
workers = 1
device = "cpu"
amp = True  # Mixed precision even on CPU (safe fallback)

# === NAMING VERSION BASED ON LIMITS ===
version = f"v_cpu_e{epochs}_img{imgsz}_b{batch}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
output_dir = os.path.join("model_weights", version)
os.makedirs(output_dir, exist_ok=True)

# === START TRAINING ===
model = YOLO(base_model)

model.train(
    data=yaml_file,
    epochs=epochs,
    imgsz=imgsz,
    batch=batch,
    workers=workers,
    device=device,
    amp=amp,
    project="model_weights",
    name=version,
    save=True
)

print(f"✅ Training completed! Model saved in: {output_dir}")
