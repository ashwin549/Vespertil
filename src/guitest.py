import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QStackedWidget, QLineEdit, QGridLayout, 
                           QFrame, QScrollArea, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
import random  # For demo data, remove in production

class ModernButton(QPushButton):
    """Custom styled button for sidebar navigation"""
    def __init__(self, text, icon_name=None):
        super().__init__(text)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setMinimumHeight(50)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 5px;
                padding: 10px;
                text-align: left;
                color: #E0E0E0;
                background: transparent;
            }
            QPushButton:checked {
                background: #2D5C7F;
                color: white;
            }
            QPushButton:hover:!checked {
                background: #1E3D53;
            }
        """)

class StatisticCard(QFrame):
    """Card widget for displaying statistics"""
    def __init__(self, title, value):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #666; font-size: 14px;")
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #333; font-size: 24px; font-weight: bold;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def update_value(self, value):
        """Update the displayed value"""
        self.value_label.setText(str(value))

class CameraCard(QFrame):
    """Card widget for camera selection"""
    def __init__(self, camera_name, camera_ip):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton {
                background: #2D5C7F;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background: #1E3D53;
            }
        """)
        self.setMinimumHeight(150)

        layout = QVBoxLayout(self)
        
        name_label = QLabel(camera_name)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        ip_label = QLabel(camera_ip)
        ip_label.setStyleSheet("color: #666;")
        
        button = QPushButton("Connect")
        
        layout.addWidget(name_label)
        layout.addWidget(ip_label)
        layout.addWidget(button)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Surveillance System")
        self.resize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background: #F5F5F5;
            }
        """)
        
        # Create main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.setup_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create different pages
        self.setup_dashboard()
        self.setup_cameras()
        self.setup_analytics()
        self.setup_settings()
        
        # Initialize with dashboard
        self.dashboard_btn.setChecked(True)
        
        # Demo: Update statistics periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_statistics)
        self.timer.start(5000)  # Update every 5 seconds

    def setup_sidebar(self):
        """Create sidebar with navigation buttons"""
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background: #1A2930;")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo/Title
        title = QLabel("Surveillance")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; padding: 10px;")
        sidebar_layout.addWidget(title)
        
        sidebar_layout.addSpacing(30)
        
        # Navigation buttons
        self.dashboard_btn = ModernButton("Dashboard")
        self.dashboard_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        self.cameras_btn = ModernButton("Cameras")
        self.cameras_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        self.analytics_btn = ModernButton("Analytics")
        self.analytics_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        self.settings_btn = ModernButton("Settings")
        self.settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        
        for btn in [self.dashboard_btn, self.cameras_btn, self.analytics_btn, self.settings_btn]:
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()

    def setup_dashboard(self):
        """Create dashboard page with statistics and quick actions"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Statistics grid
        stats_widget = QWidget()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(20)
        
        self.active_cameras = StatisticCard("Active Cameras", "4")
        self.people_detected = StatisticCard("People Detected Today", "127")
        self.alerts = StatisticCard("Active Alerts", "2")
        self.uptime = StatisticCard("System Uptime", "24h 13m")
        
        stats_layout.addWidget(self.active_cameras, 0, 0)
        stats_layout.addWidget(self.people_detected, 0, 1)
        stats_layout.addWidget(self.alerts, 1, 0)
        stats_layout.addWidget(self.uptime, 1, 1)
        
        layout.addWidget(stats_widget)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)

    def setup_cameras(self):
        """Create cameras page with camera management"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title and add camera button
        header_layout = QHBoxLayout()
        title = QLabel("Cameras")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        add_camera_btn = QPushButton("Add Camera")
        add_camera_btn.setStyleSheet("""
            QPushButton {
                background: #2D5C7F;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #1E3D53;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_camera_btn)
        layout.addLayout(header_layout)
        
        # Camera grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        camera_widget = QWidget()
        camera_layout = QGridLayout(camera_widget)
        camera_layout.setSpacing(20)
        
        # Demo cameras
        cameras = [
            ("Front Entrance", "192.168.1.101"),
            ("Back Entrance", "192.168.1.102"),
            ("Parking Lot", "192.168.1.103"),
            ("Reception", "192.168.1.104")
        ]
        
        for i, (name, ip) in enumerate(cameras):
            camera_card = CameraCard(name, ip)
            camera_layout.addWidget(camera_card, i // 2, i % 2)
        
        scroll.setWidget(camera_widget)
        layout.addWidget(scroll)
        
        self.stacked_widget.addWidget(page)

    def setup_analytics(self):
        """Create analytics page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Placeholder for graphs and charts
        layout.addWidget(QLabel("Analytics content goes here"))
        
        self.stacked_widget.addWidget(page)

    def setup_settings(self):
        """Create settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Add some sample settings
        settings = [
            ("Storage Location", "/path/to/storage"),
            ("Retention Period", "30 days"),
            ("Alert Notifications", "Enabled"),
            ("Motion Sensitivity", "Medium")
        ]
        
        for setting_name, setting_value in settings:
            setting_layout = QHBoxLayout()
            name_label = QLabel(setting_name)
            name_label.setStyleSheet("font-size: 16px; color: #333;")
            value_input = QLineEdit(setting_value)
            value_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #DDD;
                    border-radius: 5px;
                }
            """)
            
            setting_layout.addWidget(name_label)
            setting_layout.addWidget(value_input)
            layout.addLayout(setting_layout)
        
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)

    def update_statistics(self):
        """Update dashboard statistics with random demo data"""
        self.people_detected.update_value(str(random.randint(100, 200)))
        self.alerts.update_value(str(random.randint(0, 5)))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()