# CyberEDU - Ransomware Simulator

CyberEDU is an educational tool designed to demonstrate how ransomware works in a safe, controlled environment. Built with Python and PyQt6.

## Features
- **Sandbox Environment:** Operates strictly on `demo_files/` folder.
- **AES Encryption:** Real-time encryption simulation using `cryptography` library.
- **Ransom Simulation:** Custom dark-themed UI with a countdown timer and ransom note.
- **Security Researcher Mode:** One-click decryption to restore files.
- **Real-time Logs:** See exactly what happens behind the scenes.
- **Educational Content:** Learn about history and protection against ransomware.

## Installation
1. Ensure you have Python 3.x installed.
2. Install dependencies:
   ```bash
   pip install PyQt6 cryptography pyqtgraph
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Warning
This application is for **educational purposes only**. It uses a sample sandbox folder (`demo_files/`) to prevent any accidental data loss. **Never attempt to use these techniques on files outside the sandbox.**

## Educational Section
Includes:
- What is ransomware?
- Famous attacks (WannaCry, NotPetya).
- Protective measures (Backups, Patching).
