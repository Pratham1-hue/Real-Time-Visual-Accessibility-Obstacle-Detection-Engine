from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Loads PyTorch model by default. 
        # For edge optimization, pass 'yolov8n.onnx' or 'yolov8n.engine' here later.
        self.model = YOLO(model_path)

    def detect(self, frame):
        # verbose=False keeps the console clean during the video stream
        results = self.model(frame, verbose=False)
        
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()
                cls_id = int(box.cls[0].item())
                cls_name = self.model.names[cls_id]
                
                # Only return confident detections
                if conf > 0.5:
                    box_coords = [int(x1), int(y1), int(x2), int(y2)]
                    detections.append((box_coords, cls_name, conf))
                    
        return detections