import multiprocessing
try:
    from pythonjsonlogger import jsonlogger  # type: ignore
    JSONLOGGER_AVAILABLE = True
except Exception:
    JSONLOGGER_AVAILABLE = False

worker_processes = max(2, multiprocessing.cpu_count() * 2 + 1)
bind = "0.0.0.0:8000"
timeout = 30
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configure JSON formatted logs for the Gunicorn process
if JSONLOGGER_AVAILABLE:
    logconfig_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                # A string import target (dictConfig) will try to import the class at runtime
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter' if JSONLOGGER_AVAILABLE else 'logging.Formatter',
                'fmt': '%(asctime)s %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'loggers': {
            'gunicorn.error': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': False
            },
            'gunicorn.access': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': False
            }
        }
    }
# Do not use a complex dictLogConfig for Gunicorn here; keep default access/error logs to STDOUT
logconfig_dict = None
