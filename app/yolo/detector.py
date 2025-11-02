import cv2
import os
from ultralytics import YOLO

# Load models
model_firearm = YOLO(r"C:\Users\laxma\Desktop\projects\myprojects\FIREARMS_FOR_MAJOR\FILES2\model_weights\v_cpu_e10_img416_b4_20250430_2024112\weights\best.pt")      # Fine-tuned model
model_firearm.fuse()  # Fuse model layers for faster inference

model_coco = YOLO(r"C:\Users\laxma\Desktop\projects\myprojects\FIREARMS_FOR_MAJOR\FILES2\yolov8n.pt")    # COCO model
model_coco.fuse()  # Fuse model layers for faster inference


allowed_coco_classes = [
    'person', 'car', 'truck', 'bicycle', 'motorcycle', 'knife',
    'banana', 'apple', 'orange', 'fork', 'spoon', 'bowl', 'cup'
]
coco_labels = model_coco.names

# Color map for classes
color_map = {
    'Gun': (0, 0, 255),          # Red
    'person': (0, 255, 0),       # Green
    'car': (255, 0, 0),          # Blue
    'truck': (255, 255, 0),      # Cyan
    'bicycle': (255, 0, 255),    # Magenta
    'motorcycle': (0, 255, 255), # Yellow
    'knife': (0, 128, 255),      # Orange
    'banana': (20, 220, 220),    # Sky
    'apple': (0, 0, 128),        # Navy
    'orange': (255, 165, 0),     # Orange
    'fork': (128, 128, 0),       # Olive
    'spoon': (128, 0, 128),      # Purple
    'bowl': (64, 224, 208),      # Turquoise
    'cup': (160, 82, 45)         # Brown
}

def run_detection(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if input_path.lower().endswith(('.mp4', '.avi', '.mov')):
        cap = cv2.VideoCapture(input_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = min(cap.get(cv2.CAP_PROP_FPS), 100.0)  # Cap it at 100 FPS
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        result_filename = os.path.splitext(os.path.basename(input_path))[0] + "_resultvideo.mp4"
        result_path = os.path.join(output_dir, result_filename)

        out = cv2.VideoWriter(result_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result_f = model_firearm(frame)[0]
            result_c = model_coco(frame)[0]

            # Draw firearms (Gun)
            for box, cls in zip(result_f.boxes.xyxy, result_f.boxes.cls):
                class_name = model_firearm.names[int(cls)]
                color = color_map.get(class_name, (0, 0, 255))  # default to red
                x1, y1, x2, y2 = map(int, box)
                label = f"{class_name}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Draw general classes (COCO)
            for box, cls in zip(result_c.boxes.xyxy, result_c.boxes.cls):
                class_name = coco_labels[int(cls)]
                if class_name in allowed_coco_classes:
                    color = color_map.get(class_name, (255, 255, 255))  # white if no color defined
                    x1, y1, x2, y2 = map(int, box)
                    label = f"{class_name}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            out.write(frame)

        cap.release()
        out.release()
        return result_path

    else:
        result_f = model_firearm(input_path)[0]
        result_c = model_coco(input_path)[0]

        frame = cv2.imread(input_path)

        # Draw firearm detections
        for box, cls in zip(result_f.boxes.xyxy, result_f.boxes.cls):
            class_name = model_firearm.names[int(cls)]
            color = color_map.get(class_name, (0, 0, 255))  # default red
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Draw coco detections
        for box, cls in zip(result_c.boxes.xyxy, result_c.boxes.cls):
            class_name = coco_labels[int(cls)]
            if class_name in allowed_coco_classes:
                color = color_map.get(class_name, (255, 255, 255))
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        result_path = os.path.join(output_dir, f"{name}_result.jpg")
        cv2.imwrite(result_path, frame)
        return result_path



