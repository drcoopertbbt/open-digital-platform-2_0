from fastapi import FastAPI, HTTPException
import uvicorn
import requests
from contextlib import asynccontextmanager
import time
from typing import Dict

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import start_http_server

# Set up tracing
resource = Resource.create({"service.name": "amf-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
console_span_exporter = ConsoleSpanExporter()
span_processor = BatchSpanProcessor(console_span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Set up metrics
metric_reader = PrometheusMetricReader()
console_metric_exporter = ConsoleMetricExporter()
periodic_metric_reader = PeriodicExportingMetricReader(console_metric_exporter, export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader, periodic_metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Create metrics
handover_request_counter = meter.create_counter("ngap_handover_requests_total", description="Total number of NGAP Handover Requests")
handover_duration_histogram = meter.create_histogram("ngap_handover_duration_seconds", description="Duration of NGAP Handover process")

nrf_url = "http://127.0.0.1:8000"
smf_url = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global smf_url
    nf_registration = {
        "nf_type": "AMF",
        "ip": "0.0.0.0",
        "port": 9000
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()

        smf_info = requests.get(f"{nrf_url}/discover/SMF").json()
        if 'message' in smf_info:
            print(f"SMF discovery failed: {smf_info['message']}")
        else:
            smf_url = f"http://{smf_info.get('ip')}:{smf_info.get('port')}"
            print(f"SMF discovered at {smf_url}")
    except requests.RequestException as e:
        print(f"Failed to register with NRF or discover SMF: {str(e)}")

    start_http_server(9100)
    yield

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app)

# Simulated UE and gNB data
ue_contexts: Dict[str, Dict] = {}
gnb_data: Dict[str, Dict] = {
    "gnb001": {"ip": "192.168.1.1", "capacity": 100},
    "gnb002": {"ip": "192.168.1.2", "capacity": 100},
}

def handle_ngap_handover_request(request_data: Dict):
    with tracer.start_as_current_span("ngap_handover_request") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_REQUEST")
        span.set_attribute("ngap.source_gnb_id", request_data['source_gnb_id'])
        
        # Simulate processing of handover request
        ue_id = request_data['ue_id']
        if ue_id not in ue_contexts:
            raise HTTPException(status_code=404, detail="UE context not found")
        
        # Decide on target gNB (simplified logic)
        target_gnb_id = "gnb002" if request_data['source_gnb_id'] == "gnb001" else "gnb001"
        
        # Update UE context
        ue_contexts[ue_id]['target_gnb_id'] = target_gnb_id
        
        # Simulate sending NGAP Handover Request Acknowledge
        send_ngap_handover_request_ack(request_data['source_gnb_id'])
        
        return target_gnb_id

def send_ngap_handover_request_ack(source_gnb_id: str):
    with tracer.start_as_current_span("ngap_handover_request_ack") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_REQUEST_ACK")
        span.set_attribute("ngap.source_gnb_id", source_gnb_id)
        # Simulate sending acknowledgment
        time.sleep(0.01)  # Simulate network delay

def initiate_ngap_resource_setup(target_gnb_id: str):
    with tracer.start_as_current_span("ngap_resource_setup") as span:
        span.set_attribute("ngap.message_type", "NGAP_RESOURCE_SETUP_REQUEST")
        span.set_attribute("ngap.target_gnb_id", target_gnb_id)
        
        # Simulate sending resource setup request to target gNB
        time.sleep(0.02)  # Simulate network delay
        
        # Simulate receiving resource setup response
        time.sleep(0.02)  # Simulate network delay
        span.add_event("Resource setup completed")

def send_ngap_handover_command(source_gnb_id: str, target_gnb_id: str):
    with tracer.start_as_current_span("ngap_handover_command") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_COMMAND")
        span.set_attribute("ngap.source_gnb_id", source_gnb_id)
        span.set_attribute("ngap.target_gnb_id", target_gnb_id)
        
        # Simulate sending handover command to source gNB
        time.sleep(0.01)  # Simulate network delay
        
        # Wait for handover complete message
        time.sleep(0.03)  # Simulate handover execution time
        span.add_event("Handover completed")

@app.post("/amf/handover")
async def amf_handover(request_data: Dict):
    start_time = time.time()
    handover_request_counter.add(1)
    
    try:
        # Simulate receiving NGAP Handover Request
        target_gnb_id = handle_ngap_handover_request(request_data)
        
        # Simulate NGAP Resource Setup
        initiate_ngap_resource_setup(target_gnb_id)
        
        # Simulate sending NGAP Handover Command
        send_ngap_handover_command(request_data['source_gnb_id'], target_gnb_id)
        
        # Record handover duration
        duration = time.time() - start_time
        handover_duration_histogram.record(duration)
        
        return {"message": "Handover process completed", "duration": duration}
    except Exception as e:
        return {"message": f"Handover failed: {str(e)}"}

@app.get("/amf/ue/{ue_id}")
async def get_ue_context(ue_id: str):
    if ue_id not in ue_contexts:
        raise HTTPException(status_code=404, detail="UE context not found")
    return ue_contexts[ue_id]

@app.post("/amf/ue/{ue_id}")
async def create_ue_context(ue_id: str, context: Dict):
    ue_contexts[ue_id] = context
    return {"message": "UE context created"}

@app.get("/metrics")
async def metrics():
    return {"message": "Metrics are exposed on port 9100"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)