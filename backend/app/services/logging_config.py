import logging, os
try:
    from pythonjsonlogger import jsonlogger
except Exception:
    jsonlogger = None

def configure_logging(service_name='demand-forecasting', level=logging.INFO):
    fmt = '%(asctime)s %(levelname)s %(name)s %(message)s'
    handler = logging.StreamHandler()
    if jsonlogger:
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s')
    else:
        formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        root.addHandler(handler)
    # example: add structured field via adapter in requests
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)
