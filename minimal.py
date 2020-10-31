from prometheus_client import (
    CollectorRegistry,
    Gauge, Counter,
)
from pyramid.config import Configurator
from pyramid.response import Response
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
)
import random


def update(request):
    num = random.uniform(0, 1)
    request.registry["hits"].inc()
    request.registry["level"].set(num)


def metrics_web(request):
    update(request)
    registry = request.registry[
        "prometheus_registry"
    ]
    return Response(
        generate_latest(registry),
        content_type=CONTENT_TYPE_LATEST,
    )


def configure_metrics(mapping):
    registry = CollectorRegistry()
    mapping["prometheus_registry"] = registry
    mapping["level"] = Gauge(
        "level",
        "The level",
        registry=registry,
    )
    mapping["hits"] = Counter(
        "hits",
        "Hits to endpoint",
        registry=registry,
    )


with Configurator() as config:
    configure_metrics(config.registry)
    config.add_route("metrics", "/metrics")
    config.add_view(
        metrics_web, route_name="metrics"
    )
    application = config.make_wsgi_app()
