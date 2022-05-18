import os
from time import sleep

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    Resource,
    SERVICE_VERSION,
    DEPLOYMENT_ENVIRONMENT,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (  # type: ignore
    DEFAULT_TRACES_EXPORT_PATH,
    OTLPSpanExporter,
)
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)  # type: ignore
from opentelemetry.exporter.datadog import DatadogExportSpanProcessor, DatadogSpanExporter


trace_provider = TracerProvider(
    resource=Resource.create(
        {
            SERVICE_NAME: "adrian-test",
            SERVICE_VERSION: "0.1.0",
            DEPLOYMENT_ENVIRONMENT: "dev",
        }
    ),
)


trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer(__name__)


agent_host = os.environ["HOST_IP"]

trace_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

otlp_http_endpoint = f"http://{agent_host.removesuffix('/')}:4318/{DEFAULT_TRACES_EXPORT_PATH}"
trace_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(otlp_http_endpoint))
)

# trace_provider.add_span_processor(
#     DatadogExportSpanProcessor(DatadogSpanExporter(agent_url=f"http://{agent_host}:8126"))
# )



while True:
    with tracer.start_as_current_span("foo") as foo_span:
        sleep(1)
        with tracer.start_as_current_span("bar") as bar_span:
            sleep(1)
