from flask import Flask
from redis import StrictRedis
import logging
import time

#TODO: this should be in config file
redis_state = StrictRedis.from_url("redis://redis1:6379/0",decode_responses = True)
#redis_pubsub = StrictRedis.from_url("",decode_responses = False)

#initialize redis variables
redis_state.set('last_stream',str(time.time()))

app = Flask(__name__)
#app.config['REDIS_URL'] = "redis://redis:6379/0"

if __name__ != "__main__":
    #Starting gunicorn generates a logging object via getLogger("gunicorn.error") that we are accessing here directly.
    gunicorn_logger = logging.getLogger("gunicorn.error")
    #set the Flask 
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

from app import views