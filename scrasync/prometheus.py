
import request 

from .config.appconf import (
    PROMETHEUS_HOST, PROMETHEUS_PATH, PROMETHEUS_PORT, 
    RABBITMQ_METRICS_PORT, RABBITMQ_SCRASYNC_QUEUES_NAME, RPC_HOST,
    RPC_QUEUE_NAME, RPC_VHOST
)

METRICS_ENDPOINT = f"http://{RPC_HOST}:{RABBITMQ_METRICS_PORT}/api/{RPC_VHOST}/{RABBITMQ_SCRASYNC_QUEUES_NAME}"


def get_crawl_metrics(containerid: str = None, crawlid: str = None):
    """ Retrieves metrics from prometheus. """
    
    
    
    resp = requests.get(f'{PROMETHEUS_HOST}/{PROMETHEUS_PATH}?query=query')
    import remote_pdb; remote_pdb.set_trace()

    return True


