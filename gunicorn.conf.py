"""Configures gunicorn"""
import multiprocessing
from gevent_grpc_worker import GeventGrpcWorker

# http://docs.gunicorn.org/en/stable/design.html#how-many-workers
workers = multiprocessing.cpu_count() * 2 + 1
# Use an asynchronous worker as most of the work is waiting for websites to load
worker_class = '.'.join([GeventGrpcWorker.__module__,
                         GeventGrpcWorker.__name__])
loglevel = 'debug'
accesslog = 'gunicorn-access.log'
errorlog = 'gunicorn-error.log'
