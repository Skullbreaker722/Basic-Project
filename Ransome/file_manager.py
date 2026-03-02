import os
import shutil

class FileManager:
    """Handles the creation and management of the sandbox folder 'demo_files'."""

    def __init__(self, sandbox_name="demo_files"):
        self.sandbox_path = os.path.join(os.getcwd(), sandbox_name)

    def setup_sandbox(self):
        """Creates the sandbox directory and dummy files if they don't exist."""
        if not os.path.exists(self.sandbox_path):
            os.makedirs(self.sandbox_path)
            self.create_dummy_files()
        else:
            # Refresh files if directory exists but looks empty
            if not self.list_files():
                self.create_dummy_files()

    def create_dummy_files(self):
        """Populates the sandbox with various dummy file types."""
        files_to_create = {
            "proposal.txt": "Confidential Security Audit Proposal. 2026 Q1.",
            "budget_2026.csv": "Month,Amount\nJanuary,5000\nFebruary,4500",
            "db_credentials.cfg": "DB_HOST=192.168.1.10\nDB_USER=admin\nDB_PASS=S3cur3P@ss",
            "project_notes.docx": "Planning notes for the next secure infrastructure update.",
            "secrets.env": "API_KEY=vX92kLp-29xk-1029-skA21",
        }

        for filename, content in files_to_create.items():
            file_path = os.path.join(self.sandbox_path, filename)
            with open(file_path, "w") as f:
                f.write(content)

    def list_files(self):
        """Returns a list of all files in the sandbox."""
        if not os.path.exists(self.sandbox_path):
            return []
        return [f for f in os.listdir(self.sandbox_path) if os.path.isfile(os.path.join(self.sandbox_path, f))]

    def reset_sandbox(self):
        """Deletes and recreates the sandbox folder."""
        if os.path.exists(self.sandbox_path):
            shutil.rmtree(self.sandbox_path)
        self.setup_sandbox()

    def get_full_path(self, filename):
        """Helper to get absolute path of a file in sandbox."""
        return os.path.join(self.sandbox_path, filename)
