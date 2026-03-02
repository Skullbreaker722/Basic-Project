import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QListWidget, QProgressBar, 
                             QTextEdit, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor, QIcon
import pyqtgraph as pg
from encryption_engine import EncryptionEngine
from file_manager import FileManager

class CybexUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberEDU - Ransomware Simulator")
        self.resize(1000, 700)
        
        self.file_manager = FileManager()
        self.file_manager.setup_sandbox()
        self.encryption_engine = EncryptionEngine()
        
        self.init_ui()
        self.apply_styles()
        
        # Timer for ransom countdown
        self.remaining_time = 360  # 6 minutes
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #010409; }
            QWidget#sidebar { background-color: #0D1117; border-right: 1px solid #238636; }
            QLabel { color: #8B949E; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            QLabel#header { font-size: 26px; color: #39FF14; font-weight: bold; font-family: 'Consolas'; }
            QLabel#status { font-size: 16px; color: #FF3B30; }
            
            QPushButton { 
                background-color: #0D1117; 
                color: #39FF14; 
                border: 1px solid #30363D; 
                padding: 12px; 
                font-family: 'Consolas';
                border-radius: 6px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover { 
                background-color: #21262D; 
                border-color: #39FF14;
                color: #FFFFFF;
            }
            QPushButton#attack-btn { 
                background-color: #DA3633; 
                border: 1px solid #F85149; 
                color: white; 
                font-weight: bold; 
                text-align: center;
                padding-left: 12px;
            }
            QPushButton#attack-btn:hover { 
                background-color: #B62324;
                box-shadow: 0px 0px 15px rgba(255, 0, 0, 0.4);
            }
            
            QListWidget { 
                background-color: #0D1117; 
                color: #39FF14; 
                border: 1px solid #30363D; 
                font-family: 'Consolas'; 
                border-radius: 8px;
                padding: 5px;
            }
            QProgressBar { 
                border: 1px solid #30363D; 
                background-color: #0D1117; 
                height: 25px; 
                border-radius: 12px; 
                text-align: center; 
                color: #39FF14; 
                font-weight: bold;
            }
            QProgressBar::chunk { 
                background: QLinearGradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #39FF14, stop: 1 #238636); 
                border-radius: 10px; 
            }
            
            QTextEdit { 
                background-color: #0D1117; 
                color: #E6EDF3; 
                border: 1px solid #30363D; 
                font-family: 'Consolas'; 
                border-radius: 8px;
                padding: 10px;
            }
        """)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        
        logo = QLabel("CyberEDU")
        logo.setObjectName("header")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(40)
        
        btn_dash = QPushButton("Dashboard")
        btn_encrypt = QPushButton("Simulation")
        btn_edu = QPushButton("Educational")
        btn_reset = QPushButton("Reset Sandbox")
        
        btn_dash.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_encrypt.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_edu.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_reset.clicked.connect(self.reset_simulation)
        
        sidebar_layout.addWidget(btn_dash)
        sidebar_layout.addWidget(btn_encrypt)
        sidebar_layout.addWidget(btn_edu)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(btn_reset)
        sidebar_layout.addSpacing(20)
        
        main_layout.addWidget(sidebar)

        # Content Stack
        self.stack = QStackedWidget()
        
        # 1. Dashboard Page
        self.setup_dashboard()
        
        # 2. Simulation Page
        self.setup_simulation_page()
        
        # 3. Education Page
        self.setup_education_page()
        
        # 4. Ransom Page
        self.setup_ransom_page()
        
        main_layout.addWidget(self.stack)

    def setup_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("System Dashboard")
        title.setObjectName("header")
        layout.addWidget(title)
        
        stats_layout = QHBoxLayout()
        self.lbl_file_count = QLabel("Total Files: 0")
        self.lbl_encrypted_count = QLabel("Encrypted: 0")
        stats_layout.addWidget(self.lbl_file_count)
        stats_layout.addWidget(self.lbl_encrypted_count)
        layout.addLayout(stats_layout)
        
        # Graph
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#0A0A0A')
        self.plot_widget.setTitle("Encryption Monitoring", color="#00FF41")
        self.plot_widget.setLabel('left', 'Encrypted %', color="#00FF41")
        self.plot_widget.setLabel('bottom', 'Time (eval)', color="#00FF41")
        layout.addWidget(self.plot_widget)
        
        # Logs
        layout.addWidget(QLabel("Real-time Logs:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        self.stack.addWidget(page)
        self.update_stats()

    def setup_simulation_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("Ransomware Execution Control"))
        
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Sandbox Files (demo_files/):"))
        layout.addWidget(self.file_list)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.btn_attack = QPushButton("LAUNCH ATTACK")
        self.btn_attack.setObjectName("attack-btn")
        self.btn_attack.clicked.connect(self.run_attack)
        layout.addWidget(self.btn_attack)
        
        self.stack.addWidget(page)
        self.refresh_file_list()

    def setup_ransom_page(self):
        self.ransom_page = QWidget()
        self.ransom_page.setStyleSheet("background-color: #330000;")
        layout = QVBoxLayout(self.ransom_page)
        
        title = QLabel("!!! YOUR FILES ARE ENCRYPTED !!!")
        title.setFont(QFont("Consolas", 30, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF0000; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        note = QTextEdit()
        note.setReadOnly(True)
        note.setPlainText("What Happened to My Computer?\n\nYour important files are encrypted. Many of your documents, photos, videos, databases and other files are no longer accessible because they have been encrypted. Maybe you are busy looking for a way to recover your files, but do not waste your time. Nobody can recover your files without our decryption service.\n\nPayment information (Educational Demo):\nTo recover your files, you must pay $300 worth of Bitcoin.\nWallet: EDUCATIONAL_PURPOSES_ONLY_WAL_LET_123456789")
        note.setStyleSheet("background-color: #000; color: #FF0000; border: 2px solid #FF0000; font-size: 14px;")
        layout.addWidget(note)
        
        self.timer_lbl = QLabel("Time Left: 00:06:00")
        self.timer_lbl.setFont(QFont("Consolas", 20))
        self.timer_lbl.setStyleSheet("color: #FFFF00;")
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_lbl)
        
        self.btn_decrypt = QPushButton("ENTER SECURITY RESEARCHER MODE (DEBUG KEY)")
        self.btn_decrypt.setStyleSheet("background-color: #00FF41; color: black; font-weight: bold;")
        self.btn_decrypt.clicked.connect(self.run_decryption)
        layout.addWidget(self.btn_decrypt)
        
        self.stack.addWidget(self.ransom_page)

    def setup_education_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Educational Section")
        title.setObjectName("header")
        layout.addWidget(title)
        
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMarkdown("""
## What is Ransomware?
Ransomware is a type of malware that encrypts a victim's files. The attacker then demands a ransom from the victim to restore access to the data upon payment.

## Famous Ransomware Attacks
- **WannaCry (2017):** Exploited EternalBlue vulnerabilities in Windows, affecting 200k computers globally.
- **NotPetya (2017):** Initially thought to be ransomware, it was actually a wiper designed to destroy data.
- **DarkSide (2021):** Responsible for the Colonial Pipeline shutdown in the US.

## How Encryption Works
Encryption uses mathematical algorithms (like AES) and a **Key** to scramble data. Without the key, the data is just random noise.

## How to Protect Yourself
1. **Backups:** Keep offline backups of important data.
2. **Patching:** Keep OS and software up to date.
3. **Email Safety:** Be wary of attachments and links from unknown sources.
4. **EDR/AV:** Use high-quality security software.
        """)
        layout.addWidget(info)
        
        self.stack.addWidget(page)

    # --- Logic ---

    def log(self, msg):
        self.log_output.append(f"> {msg}")

    def refresh_file_list(self):
        self.file_list.clear()
        files = self.file_manager.list_files()
        self.file_list.addItems(files)
        self.update_stats()

    def update_stats(self):
        files = self.file_manager.list_files()
        total = len(files)
        encrypted = len([f for f in files if f.endswith(".encrypted")])
        self.lbl_file_count.setText(f"Total Files: {total}")
        self.lbl_encrypted_count.setText(f"Encrypted: {encrypted}")
        
    def run_attack(self):
        self.log("Initializing Ransomware Simulation...")
        self.log(f"Generated AES Key: {self.encryption_engine.key.decode()[:10]}...")
        
        files = [f for f in self.file_manager.list_files() if not f.endswith(".encrypted")]
        if not files:
            self.log("Nothing to encrypt.")
            return
        
        self.progress_bar.setMaximum(len(files))
        self.btn_attack.setEnabled(False)
        self.btn_attack.setText("ENCRYPTING...")
        
        # Simulating progress
        self.enc_index = 0
        self.enc_files = files
        
        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.process_next_encryption)
        self.attack_timer.start(500) # One file every 0.5 sec

    def process_next_encryption(self):
        if self.enc_index < len(self.enc_files):
            file_name = self.enc_files[self.enc_index]
            path = self.file_manager.get_full_path(file_name)
            if self.encryption_engine.encrypt_file(path):
                self.log(f"Encrypted: {file_name}")
            
            self.enc_index += 1
            self.progress_bar.setValue(self.enc_index)
            self.refresh_file_list()
        else:
            self.attack_timer.stop()
            self.log("Attack Complete. Displaying Ransom Note.")
            self.show_ransom_note()

    def show_ransom_note(self):
        self.stack.setCurrentWidget(self.ransom_page)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.remaining_time -= 1
        mins = self.remaining_time // 60
        secs = self.remaining_time % 60
        self.timer_lbl.setText(f"Time Left: 00:{mins:02}:{secs:02}")
        if self.remaining_time <= 0:
            self.countdown_timer.stop()
            self.timer_lbl.setText("TIME EXPIRED - DATA LOST (SIMULATED)")

    def run_decryption(self):
        self.log("Security Researcher Mode activated.")
        self.log("Using recovery key to restore files...")
        
        encrypted_files = [f for f in self.file_manager.list_files() if f.endswith(".encrypted")]
        for f in encrypted_files:
            path = self.file_manager.get_full_path(f)
            if self.encryption_engine.decrypt_file(path):
                self.log(f"Decrypted: {f.replace('.encrypted', '')}")
        
        self.log("All files recovered successfully.")
        self.countdown_timer.stop()
        self.remaining_time = 360
        self.btn_attack.setEnabled(True)
        self.btn_attack.setText("LAUNCH ATTACK")
        self.stack.setCurrentIndex(0)
        self.refresh_file_list()

    def reset_simulation(self):
        self.file_manager.reset_sandbox()
        self.encryption_engine = EncryptionEngine() # New key
        self.log("Sandbox reset. State cleared.")
        self.refresh_file_list()
        self.stack.setCurrentIndex(0)
        self.btn_attack.setEnabled(True)
        self.btn_attack.setText("LAUNCH ATTACK")
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CybexUI()
    window.show()
    sys.exit(app.exec())
