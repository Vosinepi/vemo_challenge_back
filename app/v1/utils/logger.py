import sys
from apscheduler.schedulers.background import BackgroundScheduler
import logging


sys.path.append(".")

# Configuro el logging
handler = logging.FileHandler("app/v1/logs/schedule_mail_ddbb.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
