import cv2
from core.detector import ObjectDetector
from core.distance import estimate_distance
from audio.feedback import AudioFeedback

def main():
    detector = ObjectDetector(model_path="yolov8n.pt")
    audio = AudioFeedback(cooldown=4.0)
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        
        for box, cls_name, conf in detections:
            dist = estimate_distance(box)
            
            # Draw bounding box and info for debugging
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{cls_name} {dist:.1f}m"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Filter high-priority alert cues (e.g., object is closer than 1.5 meters)
            if dist < 1.5:
                audio.play_alert(f"{cls_name} ahead")

        cv2.imshow("Obstacle Engine", frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()