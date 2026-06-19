"""OpenTelemetry wiring template (FastAPI / Python).

Copy into your app (e.g. app/telemetry.py) and call setup_telemetry(app) once at
startup. Mirrors examples/minimal-service/telemetry.py in the kit and the
reference solution's backend/app/telemetry.py.

Satisfies doctor.py's OTel check and makes the observability/ overlay show real
traces (Jaeger) and metrics (Prometheus /metrics). Set OTEL_ENABLED=false to
skip — do this in unit tests.

Requires (add to requirements.txt):
    opentelemetry-sdk opentelemetry-api
    opentelemetry-instrumentation-fastapi
    opentelemetry-exporter-otlp-proto-grpc
    opentelemetry-exporter-prometheus prometheus-client
"""
import os


def setup_telemetry(app) -> None:
    if os.environ.get("OTEL_ENABLED", "true").lower() == "false":
        return

    from opentelemetry import metrics, trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.semconv.resource import ResourceAttributes
    from prometheus_client import make_asgi_app

    endpoint = os.environ.get("OTLP_ENDPOINT", "http://jaeger:4317")
    resource = Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: os.environ.get("OTEL_SERVICE_NAME", "app"),
            ResourceAttributes.SERVICE_VERSION: "0.1.0",
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development",
        }
    )

    # Traces -> OTLP -> Jaeger
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(tracer_provider)

    # Metrics -> Prometheus (/metrics scrape endpoint)
    reader = PrometheusMetricReader()
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))

    FastAPIInstrumentor.instrument_app(app)
    app.mount("/metrics", make_asgi_app())
