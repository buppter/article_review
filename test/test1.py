from flask import Flask
from flask_caching import Cache
import datetime

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': '10.112.214.168', 'CACHE_REDIS_PORT': 6379,
                           'CACHE_REDIS_DB': '', 'CACHE_REDIS_PASSWORD': ''})


@app.route('/')
def hello():
    return "hello, world!"


@app.route('/t')
@cache.cached(timeout=10)
def cached_page():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "hello, world, what's your name, thank you!!...  localtime: " + time


if __name__ == '__main__':
    app.run()
