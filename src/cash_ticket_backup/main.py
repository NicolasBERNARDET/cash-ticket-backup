from dotenv import load_dotenv
from flask import Flask

from src.cash_ticket_backup.blueprints.upload import upload_blueprint
from src.cash_ticket_backup.utils.log_setup import setup_logging

app = Flask(__name__)

app.register_blueprint(upload_blueprint)

load_dotenv()
setup_logging()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
