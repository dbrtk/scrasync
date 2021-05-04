#!/bin/sh

celery -A djproject.app worker --loglevel=INFO -Q scrasync
