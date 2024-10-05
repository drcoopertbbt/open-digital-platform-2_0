from fastapi import FastAPI
import uvicorn
import requests
from contextlib import asynccontextmanager
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

nrf_url = "http://127.0.0.1:8000"
smf_url = None

# Initialize OpenTelemetry MeterProvider
metric_reader = PrometheusMetricReader()
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Define OpenTelemetry metrics
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

app = FastAPI(lifespan=lifespan)

@app.get("/amf_service")
def amf_service():
    # Record a metric for the request count
    request_count.add(1)

    # Simulate a latency measurement
    with request_latency_histogram.record():
        # Business logic can go here
        return {"message": "AMF service response"}

@app.get("/metrics")
def metrics_endpoint():
    # The metrics are automatically exposed on /metrics by PrometheusMetricReader
    return {"message": "Metrics are exposed on port 9100"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
