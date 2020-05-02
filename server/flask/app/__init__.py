from flask import Flask
from redis import StrictRedis
import logging
#from flask_sse import sse

redis_store = StrictRedis.from_url("redis://redis:6379/0",decode_responses=True)

app = Flask(__name__)
#app.config['REDIS_URL'] = "redis://redis:6379/0"
#app.register_blueprint(sse,url_prefix='/stream')

#redis_store.init_app(app)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

from app import views