from prometheus_client import Counter, start_http_server
import time

request_count = Counter('request_count', 'Total number of requests', labelnames=['method', 'endpoint'])
error_count = Counter('error_count', 'Total number of errors', labelnames=['method', 'endpoint'])

# count the number of requests
def increment_request_count(method, endpoint):
    request_count.labels(method,endpoint).inc()

# count the number of errors
def increment_error_count(method, endpoint):
    error_count.labels(method,endpoint).inc()

# Mixin to count requests and errors for class-based views
class MetricsMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            increment_error_count(request.method, request.path)
            raise e
        increment_request_count(request.method, request.path)
        return response

# if __name__ == '__main__':
# # Start a Prometheus HTTP server on a separate thread
#     print("Starting Prometheus metrics server on port 8090...")
#     start_http_server(8090)
#     # while True:
#     #         time.sleep(1)