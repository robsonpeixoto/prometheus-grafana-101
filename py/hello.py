from gevent import monkey
monkey.patch_all()

import random
import time

from flask import Flask, Response
from gevent.wsgi import WSGIServer
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,  # Summary
    Gauge,
    generate_latest)
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

REDIS_COUNT = Counter(
    'redis_hit_number',
    'Quantidade de vezes que o redis foi acessado')

REDIS_TIME = Histogram(
    'redis_inc_seconds',
    'Tempo necessario para incrementar uma chave no redis',
    buckets=(0.0005, 0.001, .005, .01))

REQUEST_TIME = Histogram(
    'tempo_requisicao_segundos',
    'Tempo da requisicao em segundos',
    buckets=(.001, .005, .01, .025, .05, .075, .1, .25, .5))

INPROGRESS_REQUEST = Gauge(
    'quantidade_requisicoes_andamento',
    'Quantidade de requisicoes em andamento')

@app.route('/')
@REQUEST_TIME.time()
@INPROGRESS_REQUEST.track_inprogress()
def hello():
    with REDIS_TIME.time():
        REDIS_COUNT.inc()
        count = redis.incr('hits')
    time.sleep(random.uniform(0.01, 0.4))
    return 'Essa página foi vista {} vezes\n'.format(count)

@app.route('/metrics')
def metrics():
    data = generate_latest()
    return Response(
        data,
        mimetype=CONTENT_TYPE_LATEST, )

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
