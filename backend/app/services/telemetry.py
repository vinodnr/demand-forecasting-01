import os, logging
# OpenTelemetry setup for FastAPI and workers (OTLP exporter)
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
except Exception:
    trace = None

def init_tracing(app=None, service_name='demand-forecasting-backend', otlp_endpoint=None):
    """Initialize OpenTelemetry tracing. Call early in app startup.
    If opentelemetry packages are not installed, this becomes a no-op."""
    if trace is None:
        logging.getLogger('telemetry').warning('OpenTelemetry packages not installed; tracing disabled')
        return None
    otlp = otlp_endpoint or os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')
    resource = Resource.create(attributes={"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    exporter = OTLPSpanExporter(endpoint=otlp) if otlp else OTLPSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)
    if app is not None:
        try:
            FastAPIInstrumentor.instrument_app(app)
            RequestsInstrumentor().instrument()
        except Exception as e:
            logging.getLogger('telemetry').exception('Failed to instrument FastAPI: %s', e)
    return provider
