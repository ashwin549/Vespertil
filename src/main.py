import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from ultralytics import YOLO

class VideoThread(QThread):
    """Thread for handling video capture without blocking GUI"""
    frame_ready = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        #self._running = True
        self.model=YOLO('yolov8n.pt')
        self.camera_url = "rtsp://192.168.1.2:554/live"
    
    def run(self):
        # Capture from default camera (0)
        self._running = True
        cap = cv2.VideoCapture(self.camera_url)
        while self._running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                results = self.model(frame)
                
                # Get bounding boxes, classes and confidence scores
                boxes = results[0].boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]  # Get box coordinates
                    conf = box.conf[0]  # Confidence score
                    cls = box.cls[0]    # Class id
                    
                    # Draw rectangle and label
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f'{self.model.names[int(cls)]} {conf:.2f}', 
                                (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, 
                                (0, 255, 0), 2)
                
                self.frame_ready.emit(frame)
        cap.release()
    
    def stop(self):
        self._running = False
        self.wait()

class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Processor")
        self.setup_ui()
        
        # Initialize video handling
        self.video_thread = VideoThread()
        self.video_thread.frame_ready.connect(self.update_frame)
    
    def setup_ui(self):
        # Create main widget and layout
        self.resize(800,600)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create video display
        self.display_label = QLabel()
        self.display_label.setScaledContents(True) 
        layout.addWidget(self.display_label, stretch=1) 
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_video)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)

    def start_video(self):
        """Start video capture"""
        self.video_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_video(self):
        """Stop video capture"""
        self.video_thread.stop()
                    #self.display_label.clear()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def update_frame(self, frame):
        """Update the display with a new frame"""
        # Convert frame to format suitable for Qt
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.display_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def closeEvent(self, event):
        """Handle application shutdown"""
        self.video_thread.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()