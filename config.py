import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
INTERMEDIATE_FILES_FOLDER = os.path.join(BASE_DIR, "static/intrf")
MAX_CONTENT_LENGTH = 20 * 1024 * 1024
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if os.path.exists(UPLOAD_FOLDER):
    os.chmod(UPLOAD_FOLDER, 0o755)