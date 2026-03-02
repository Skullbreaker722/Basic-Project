import sys
from PyQt6.QtWidgets import QApplication
from main_ui import CybexUI

def main():
    """Main entry point for the CyberEDU Ransomware Simulator."""
    app = QApplication(sys.argv)
    
    # Set global application properties
    app.setApplicationName("CyberEDU Ransomware Simulator")
    app.setApplicationVersion("1.0.0")
    
    # Initialize and show main UI
    window = CybexUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
