import logging

import requests
from flask import Flask, request

from opencensus.common.monitored_resource import monitored_resource
from opencensus.stats import aggregation, measure, stats, view
from opencensus.stats.exporters import stackdriver_exporter
from opencensus.tags import TagMap


def project_id():
  r = requests.get('http://metadata/computeMetadata/v1/project/project-id',
                   headers={'Metadata-Flavor': 'Google'}, timeout=2)
  return r.text

app = Flask(__name__)

PARAM_TAG = 'param'

m_requests = measure.MeasureInt("app/requests", "Number of requests", "1")
requests_view = view.View("opencensus-example/app/requests",
                          "The sum of requests",
                          [PARAM_TAG], m_requests, aggregation.SumAggregation())

op_stats = stats.Stats()
exporter = stackdriver_exporter.new_stats_exporter(stackdriver_exporter.Options(
  project_id=project_id()))
op_stats.view_manager.register_exporter(exporter)
op_stats.view_manager.register_view(requests_view)


@app.route('/')
def hello_world():
  logging.info('OpenCensus monitored resource: "%s"',
               monitored_resource.get_instance())
  mmap = op_stats.stats_recorder.new_measurement_map()
  mmap.measure_int_put(m_requests, 1)
  tmap = TagMap()
  param = request.args.get('param')
  if param:
    tmap.insert(PARAM_TAG, param)
  mmap.record(tmap)

  return 'Hello, World!'
