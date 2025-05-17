# Steps to add/install open-telemetry stuffs using UV
```bash
1. uv add opentelemetry-distro
2. Get the list of requred installation form this command
   opentelemetry-bootstrap -a requirements
3. From above step#2 we will get list which we can use uv add to install it like below
    uv add opentelemetry-instrumentation-asyncio==0.54b1 \
    opentelemetry-instrumentation-dbapi==0.54b1 \
    opentelemetry-instrumentation-logging==0.54b1 \
    opentelemetry-instrumentation-sqlite3==0.54b1 \
    opentelemetry-instrumentation-threading==0.54b1 \
    opentelemetry-instrumentation-urllib==0.54b1 \
    opentelemetry-instrumentation-wsgi==0.54b1 \
    opentelemetry-instrumentation-asgi==0.54b1 \
    opentelemetry-instrumentation-click==0.54b1 \
    opentelemetry-instrumentation-fastapi==0.54b1 \
    opentelemetry-instrumentation-httpx==0.54b1 \
    opentelemetry-instrumentation-psycopg2==0.54b1 \
    opentelemetry-instrumentation-sqlalchemy==0.54b1 \
    opentelemetry-instrumentation-starlette==0.54b1 \
    opentelemetry-instrumentation-tortoiseorm==0.54b1
```

# Step to run the service with the OTEL logging enables
```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
      --traces_exporter console \
      --metrics_exporter console \
      --logs_exporter console \
      --service_name clean-architecture-fastapi-server \
      uvicorn src.main:app
```

NOTE:

`OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true` this step enables/prints
all of the loggings, tracing and everything inside our console.
And, `opentelemetry-instrument` requires parameters what needed to be instrumented and to which place

This part:
```bash
opentelemetry-instrument \
      --traces_exporter console \
      --metrics_exporter console \
      --logs_exporter console \
      --service_name clean-architecture-fastapi-server
```
tells that instrumentation should be enabled for `traces`, `metrics` and `log_exporter` for console logging

WARNING:
We should avoid putting `--reload` while running the `uvicorn` command, as this will interfear with the open-telemetry


# Jaeger UI - To Get Open Telemetry Data exported by applications
We need Docker to spin-up the Jeager app

Docker Command:
```bash
docker run --rm \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
```

# Now, exporting the data from the Fastapi application to the Jaeger
Using the `Opentelemetry's OTEL Exporter`
```bash
uv add opentelemetry-exporter-otlp-proto-grpc
```

Now, we need to use different command to run the fastapi app (using uvicorn) with OTEL export enables
```bash
opentelemetry-instrument --service_name clean-architecture-fastapi-server.apis uvicorn src.main:app
```

# Export Custom Metrics data to the OTEL UI
To achieve this we need to import and use following code in the `main.py` file
```py
from opentelemetry import trace

tracer = trace.get_tracer("clean-architecture-fastapi-server.tracer")
```
And add the Context manager where we need to send the custom data to the OTEL UI
```python
def roll():
    with tracer.start_as_current_span("clean_architecture") as clean_architecture_span:
        result =  randint(1, 6)
        clean_architecture_span.set_attribute("clean_architecture.value", result)
        return result
```
Run the command with different service name to test and check velue in the UI side:
```bash
opentelemetry-instrument --service_name clean_architecture.apis2 uvicorn src.main:app
```

⚠️CURRENT ISSUE:
While running the app with the above command, getting following error
which we need to fix!
```text
(clean_architecture) ➜  clean_architecture git:(main) ✗ opentelemetry-instrument --service_name clean_architecture.apis2 uvicorn src.main:app
INFO:     Started server process [50432]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
INFO:     127.0.0.1:58820 - "GET /rolldice HTTP/1.1" 200 OK
ERROR:opentelemetry.exporter.otlp.proto.grpc.exporter:Failed to export metrics to localhost:4317, error code: StatusCode.UNIMPLEMENTED
ERROR:opentelemetry.exporter.otlp.proto.grpc.exporter:Failed to export metrics to localhost:4317, error code: StatusCode.UNIMPLEMENTED
ERROR:opentelemetry.exporter.otlp.proto.grpc.exporter:Failed to export metrics to localhost:4317, error code: StatusCode.UNIMPLEMENTED
```