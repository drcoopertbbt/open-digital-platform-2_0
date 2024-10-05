from fastapi import FastAPI
import uvicorn
import requests
from contextlib import asynccontextmanager
import time

# OpenTelemetry imports
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from prometheus_client import start_http_server
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

nrf_url = "http://127.0.0.1:8000"
smf_url = None

# Initialize OpenTelemetry for Tracing and Metrics
resource = Resource.create({"service.name": "amf-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Setup tracing to console (you can replace this with a Jaeger or Zipkin exporter later)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize OpenTelemetry MeterProvider for Metrics
metric_reader = PrometheusMetricReader()
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Define OpenTelemetry Metrics
request_count = meter.create_counter(
    name="amf_requests_total",
    description="Total AMF requests",
    unit="1"
)

request_latency_histogram = meter.create_histogram(
    name="amf_request_latency_seconds",
    description="AMF request latency",
    unit="s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global smf_url
    nf_registration = {
        "nf_type": "AMF",
        "ip": "0.0.0.0",  # Bind to all interfaces
        "port": 9000
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()

        # Discover SMF
        smf_info = requests.get(f"{nrf_url}/discover/SMF").json()
        if 'message' in smf_info:
            print(f"SMF discovery failed: {smf_info['message']}")
        else:
            smf_url = f"http://{smf_info.get('ip')}:{smf_info.get('port')}"
            print(f"SMF discovered at {smf_url}")
    except requests.RequestException as e:
        print(f"Failed to register with NRF or discover SMF: {str(e)}")

    # Start Prometheus metrics server on port 9100
    start_http_server(9100, addr="0.0.0.0")

    yield

    # Cleanup code can go here if needed

app = FastAPI(lifespan=lifespan)

# Automatically instrument FastAPI with OpenTelemetry tracing
FastAPIInstrumentor.instrument_app(app)

@app.get("/amf_service")
def amf_service():
    # Start a trace span for this request
    with tracer.start_as_current_span("amf_service_request") as span:
        # Record a metric for the request count
        request_count.add(1)

        # Simulate business logic and measure latency
        start_time = time.time()

        # Simulate the business logic or process
        span.add_event("Processing handover request")
        response = {"message": "AMF service response"}

        # Measure and record the latency
        latency = time.time() - start_time
        request_latency_histogram.record(latency)
        span.set_attribute("latency", latency)

        return response

@app.get("/metrics")
def metrics_endpoint():
    # The metrics are automatically exposed on /metrics by PrometheusMetricReader
    return {"message": "Metrics are exposed on port 9100"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)