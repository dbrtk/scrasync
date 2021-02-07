
import json

import requests
#from prometheus_api_client import PrometheusConnect

from .config.appconf import (
    RABBITMQ_METRICS_PORT, RABBITMQ_PROM_METRICS_PORT,
    RABBITMQ_SCRASYNC_QUEUE_NAME, RPC_HOST,
    RPC_QUEUE_NAME, RPC_PASS, RPC_USER, RPC_VHOST
)

# METRICS_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_METRICS_PORT}/api"
# these are metrics exposed by rabbitmq through the management plugins.
METRICS_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_METRICS_PORT}/api/queues/{RPC_VHOST}/{RABBITMQ_SCRASYNC_QUEUE_NAME}"


# these is an endpoint for metrics that are exposed 
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
    endpoint = '{prom_endpoint}/query?query={metrics}'.format(
        prom_endpoint=PROM_ENDPOINT,
        metrics='rabbitmq_queue_messages_unacked'
    )
    print(f'\nInside get_crawl_metrics with containerid]: {containerid}',
          flush=True)
    print(f'\nEndpoint: {endpoint}', flush=True)
    resp = requests.get(endpoint)
    print(resp, flush=True)
    try:
        return resp.json()
    except json.decoder.JSONDecodeError as err:
        return { 'msg': resp.text }
    
    #import remote_pdb; remote_pdb.RemotePdb('0.0.0.0', 4444).set_trace()

    #return resp.content
    
    
def get_tasks_in_queue(containerid: str = None, crawlid: str = None):
    """ Querying the rabbitmq metrics endpoint in order to get tasks being
        executed on the queue specified in the url (defined as 
        METRICS_ENDPOINT).
    """
    endpoint = f'{METRICS_ENDPOINT}/get'

    print(f'Endpoint: {endpoint}; User: {RPC_USER}; Pass: {RPC_PASS}', flush=True)

    resp = requests.post(
        endpoint,
        data=json.dumps({
            "count": -1,
            "ackmode": "ack_requeue_true",
            "encoding": "auto",
            "truncate": 50000
        }),
        headers={'Content-Type': 'application/json'},
        auth=(RPC_USER, RPC_PASS)
    )
    print(f'Response: {resp}; Status Code: {resp.status_code}', flush=True)

    # import remote_pdb; remote_pdb.RemotePdb('0.0.0.0', 4444).set_trace()

    try:
        out = resp.json()
    except json.decoder.JSONDecodeError as err:
        out = { 'msg': resp.text }
    print(f'OUT: {out}', flush=True)
    return out
