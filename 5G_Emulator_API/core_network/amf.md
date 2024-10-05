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