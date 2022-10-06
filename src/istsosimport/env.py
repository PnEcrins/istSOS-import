from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
flask_mail = Mail()
migrate = Migrate()

ROOT_DIR = Path(__file__).absolute().parent.parent.parent
STATIC_DIR = ROOT_DIR / "src" / "istsosimport" / "static"
FILE_ERROR_DIRECTORY = STATIC_DIR / "error_files"
DEFAULT_CONFIG_FILE = ROOT_DIR / "config.toml"
