import os

worker_class = "uvicorn.workers.UvicornWorker"
workers = 1

bind = "0.0.0.0:3000"
forwarded_allow_ips = "*"
accesslog = "-"

max_requests = 10000
max_requests_jitter = 2000
