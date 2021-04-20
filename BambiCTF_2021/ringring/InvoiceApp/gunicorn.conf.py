import multiprocessing

worker_class = "eventlet"
workers = multiprocessing.cpu_count()*2+1
keepalive = 10

bind = "0.0.0.0:7354"
