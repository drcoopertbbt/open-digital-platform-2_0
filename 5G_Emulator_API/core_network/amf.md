## To Do

- OpenTelemetry tracing and Prometheus metrics, while deferring the integration of persistent tracing storage (like Jaeger or Zipkin) to a later stage


## Notes

AMF service is working correctly! Let's break down what we can see from the output:

1. The first `curl` command to `http://localhost:9000/amf_service` didn't show any output, but it didn't show any errors either. This is likely because the AMF service is responding, but we're not printing the response in the terminal.

2. The second `curl` command to `http://localhost:9100/metrics` shows a lot of metrics, which is great. Prometheus metrics exporter is working correctly. Let's look at some key metrics:

a. `amf_requests_total 1.0`: AMF service has received one request, which corresponds to the first curl command.

b. `amf_request_latency_seconds_*`: These metrics show the latency of the AMF request. The `sum` value is very low (about 15 microseconds), which is expected for a simple operation.

c. `http_server_duration_milliseconds_*`: These metrics show details about the HTTP request duration, confirming that a request was made to `/amf_service`.

d. `target_info`: This shows that the service name is correctly set to "amf-service".

e. Various system metrics like `process_cpu_seconds_total`, `process_open_fds`, etc., which give information about the process running the AMF service.

3. The presence of these metrics indicates that both the FastAPI application and the OpenTelemetry instrumentation are working correctly.

To improve this setup:

1. Add some logging in the AMF service to see what's happening when a request is made.
2. Modify the `/amf_service` endpoint to return a more detailed response, which  could then see when making a curl request.
3. Set up a Prometheus server to scrape these metrics and visualize them over time.
4. Consider adding more custom metrics that are specific to AMF service's functionality.

AMF service appears to be running correctly with metrics properly exposed.


### notes


Create a UE context

```
curl -X POST http://localhost:9000/amf/ue/ue001 -H "Content-Type: application/json" -d '{"initial_gnb_id": "gnb001"}'
```

Initiate a handover

```
curl -X POST http://localhost:9000/amf/handover -H "Content-Type: application/json" -d '{"ue_id": "ue001", "source_gnb_id": "gnb001"}'
```

Check metrics

```
curl http://localhost:9100/metrics
```


### Output

```bash
student@telcocloud open-digital-platform-2_0]$ curl -X POST http://localhost:9000/amf/ue/ue001 -H "Content-Type: application/json" -d '{"initial_gnb_id": "gnb001"}'
{"message":"UE context created"}[student@telcocloud open-digital-platform-2_0]$ 
[student@telcocloud open-digital-platform-2_0]$ 
[student@telcocloud open-digital-platform-2_0]$ curl -X POST http://localhost:9000/amf/handover -H "Content-Type: application/json" -d '{"ue_id": "ue001", "source_gnb_id": "gnb001"}'
{"message":"Handover process completed","duration":0.09120726585388184}[student@telcocloud open-digital-platform-2_0]$ 
[student@telcocloud open-digital-platform-2_0]$ 
[student@telcocloud open-digital-platform-2_0]$ curl http://localhost:9100/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 5448.0
python_gc_objects_collected_total{generation="1"} 4583.0
python_gc_objects_collected_total{generation="2"} 1263.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 205.0
python_gc_collections_total{generation="1"} 18.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="9",version="3.11.9"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.76795136e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 6.7862528e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.72816626032e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.7999999999999999
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 11.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP target_info Target metadata
# TYPE target_info gauge
target_info{service_name="amf-service",telemetry_sdk_language="python",telemetry_sdk_name="opentelemetry",telemetry_sdk_version="1.27.0"} 1.0
# HELP http_server_active_requests Number of active HTTP server requests.
# TYPE http_server_active_requests gauge
http_server_active_requests{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000"} 0.0
# HELP http_server_duration_milliseconds Duration of HTTP server requests.
# TYPE http_server_duration_milliseconds histogram
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="0.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="25.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="50.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="75.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="100.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="250.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="750.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="1000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="2500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="7500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="+Inf",net_host_port="9000"} 1.0
http_server_duration_milliseconds_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 1.0
http_server_duration_milliseconds_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 3.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="0.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="25.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="50.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="75.0",net_host_port="9000"} 0.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="100.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="250.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="750.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="1000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="2500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="7500.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10000.0",net_host_port="9000"} 1.0
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="+Inf",net_host_port="9000"} 1.0
http_server_duration_milliseconds_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 1.0
http_server_duration_milliseconds_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 94.0
# HELP http_server_response_size_bytes measures the size of HTTP response messages (compressed).
# TYPE http_server_response_size_bytes histogram
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="0.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="25.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="50.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="75.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="100.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="250.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="750.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="1000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="2500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="7500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="+Inf",net_host_port="9000"} 1.0
http_server_response_size_bytes_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 1.0
http_server_response_size_bytes_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 32.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="0.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="25.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="50.0",net_host_port="9000"} 0.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="75.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="100.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="250.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="750.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="1000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="2500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="7500.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10000.0",net_host_port="9000"} 1.0
http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="+Inf",net_host_port="9000"} 1.0
http_server_response_size_bytes_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 1.0
http_server_response_size_bytes_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 71.0
# HELP http_server_request_size_bytes Measures the size of HTTP request messages (compressed).
# TYPE http_server_request_size_bytes histogram
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="0.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="25.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="50.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="75.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="100.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="250.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="750.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="1000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="2500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="5000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="7500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="10000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",le="+Inf",net_host_port="9000"} 1.0
http_server_request_size_bytes_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 1.0
http_server_request_size_bytes_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/ue/{ue_id}",net_host_port="9000"} 28.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="0.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="25.0",net_host_port="9000"} 0.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="50.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="75.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="100.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="250.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="750.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="1000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="2500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="5000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="7500.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="10000.0",net_host_port="9000"} 1.0
http_server_request_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",le="+Inf",net_host_port="9000"} 1.0
http_server_request_size_bytes_count{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 1.0
http_server_request_size_bytes_sum{http_flavor="1.1",http_host="127.0.0.1:9000",http_method="POST",http_scheme="http",http_server_name="localhost:9000",http_status_code="200",http_target="/amf/handover",net_host_port="9000"} 45.0
# HELP ngap_handover_requests_total Total number of NGAP Handover Requests
# TYPE ngap_handover_requests_total counter
ngap_handover_requests_total 1.0
# HELP ngap_handover_duration_seconds Duration of NGAP Handover process
# TYPE ngap_handover_duration_seconds histogram
ngap_handover_duration_seconds_bucket{le="0.0"} 0.0
ngap_handover_duration_seconds_bucket{le="5.0"} 1.0
ngap_handover_duration_seconds_bucket{le="10.0"} 1.0
ngap_handover_duration_seconds_bucket{le="25.0"} 1.0
ngap_handover_duration_seconds_bucket{le="50.0"} 1.0
ngap_handover_duration_seconds_bucket{le="75.0"} 1.0
ngap_handover_duration_seconds_bucket{le="100.0"} 1.0
ngap_handover_duration_seconds_bucket{le="250.0"} 1.0
ngap_handover_duration_seconds_bucket{le="500.0"} 1.0
ngap_handover_duration_seconds_bucket{le="750.0"} 1.0
ngap_handover_duration_seconds_bucket{le="1000.0"} 1.0
ngap_handover_duration_seconds_bucket{le="2500.0"} 1.0
ngap_handover_duration_seconds_bucket{le="5000.0"} 1.0
ngap_handover_duration_seconds_bucket{le="7500.0"} 1.0
ngap_handover_duration_seconds_bucket{le="10000.0"} 1.0
ngap_handover_duration_seconds_bucket{le="+Inf"} 1.0
ngap_handover_duration_seconds_count 1.0
ngap_handover_duration_seconds_sum 0.09120726585388184
[student@telcocloud open-digital-platform-2_0]$ 



```