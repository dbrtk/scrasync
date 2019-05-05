
import os

from scrasync.app import create_app


os.environ['PROXIMITYBOT_ENDPOINT'] = 'localhost:8000'
os.environ['REDIS_HOST_NAME'] = 'localhost'

app = create_app()

