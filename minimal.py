from prometheus_client import CollectorRegistry, Gauge
from pyramid.config import Configurator
from pyramid.response import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import random

def registry_from_num(num):
    registry = CollectorRegistry()
    g = Gauge("level", "The level", registry=registry)
    g.set(num)
    return registry

def metrics_web(request):
    num = random.uniform(0, 1)
    registry = registry_from_num(num)
    return Response(generate_latest(registry),
                    content_type=CONTENT_TYPE_LATEST)

with Configurator() as config:
    config.add_route('metrics', '/metrics')
    config.add_view(metrics_web, route_name='metrics')
    application = config.make_wsgi_app()
