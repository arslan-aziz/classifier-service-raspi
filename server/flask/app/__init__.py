from flask import Flask
from redis import StrictRedis
#from flask_sse import sse

redis_store = StrictRedis.from_url("redis://redis:6379/0",decode_responses=True)

app = Flask(__name__)
#app.config['REDIS_URL'] = "redis://redis:6379/0"
#app.register_blueprint(sse,url_prefix='/stream')

#redis_store.init_app(app)

from app import views