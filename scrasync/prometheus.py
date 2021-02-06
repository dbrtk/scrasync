
import json

import requests
#from prometheus_api_client import PrometheusConnect

from .config.appconf import (
    RABBITMQ_METRICS_PORT, RABBITMQ_PROM_METRICS_PORT,
    RABBITMQ_SCRASYNC_QUEUE_NAME, RPC_HOST,
    RPC_QUEUE_NAME, RPC_PASS, RPC_USER, RPC_VHOST
)

# METRICS_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_METRICS_PORT}/api"

METRICS_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_METRICS_PORT}/api/queues/{RPC_VHOST}/{RABBITMQ_SCRASYNC_QUEUE_NAME}"

# prometheus metrics served by rabbitmq on the port: 15692
PROM_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_PROM_METRICS_PORT}/metrics"


#def get_crawl_metrics(containerid: str = None, crawlid: str = None):

    #url = f"http://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RABBITMQ_PROM_METRICS_PORT}/metrics"
    #prom = PrometheusConnect(url=url, disable_ssl=True)
    #metrics = prom.all_metrics()
    #print(f'\nmetrics: {metrics}', flush=True)
    #print(f'\nmetrics type: {type(metrics)}', flush=True)

    #return { 'msg': metrics }


def get_crawl_metrics(containerid: str = None, crawlid: str = None):
    """ Retrieves metrics from prometheus. """

    # resp = requests.get(METRICS_ENDPOINT, auth=(RPC_USER, RPC_PASS))

    resp = requests.get(PROM_ENDPOINT)

    print(resp, flush=True)
    try:
        return resp.json()
    except json.decoder.JSONDecodeError as err:
        return { 'msg': resp.text }
    
    #import remote_pdb; remote_pdb.RemotePdb('0.0.0.0', 4444).set_trace()

    #return resp.content


