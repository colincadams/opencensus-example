"""Provides a gevent worker that also patches grpc to be asynchronous.

Note: This must be a the top level and called before any recidiviz code so that
nothing is imported prior to being patched. If it is placed inside of the
recidiviz directory, then the __init__.py file will be called first.
"""
from gunicorn.workers.ggevent import GeventWorker
from grpc.experimental import gevent


class GeventGrpcWorker(GeventWorker):
    def patch(self):
        super(GeventGrpcWorker, self).patch()
        gevent.init_gevent()
        self.log.info('patched grpc')
