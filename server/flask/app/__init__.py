from flask import Flask
from redis import StrictRedis

#redis_store = FlaskRedis.from_custom_provider(StrictRedis)
redis_store = StrictRedis.from_url("redis://redis:6379/0",decode_responses=True)

app = Flask(__name__)
#app.config['REDIS_URL'] = "redis://redis:6379/0"
data = ""

#redis_store.init_app(app)


from app import views