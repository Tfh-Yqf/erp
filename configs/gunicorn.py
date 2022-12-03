import multiprocessing


bind = 'http://localhost:8000'
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
daemon = True
