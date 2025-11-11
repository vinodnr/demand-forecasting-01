# backend/workers/jobs.py - simple Redis-backed queue using RPUSH / BLPOP
import os, json, redis, time
redis_url = os.getenv('REDIS_URL','redis://localhost:6379/0')
r = redis.from_url(redis_url)
QUEUE = os.getenv('CONVERT_QUEUE','convert:jobs')

def enqueue(job):
    r.rpush(QUEUE, json.dumps(job))
    return True

def worker_loop(process_fn):
    print('Worker loop started, listening on', QUEUE)
    while True:
        item = r.blpop(QUEUE, timeout=5)
        if not item:
            time.sleep(1)
            continue
        payload = item[1]
        job = json.loads(payload)
        print('Got job', job)
        try:
            process_fn(job)
        except Exception as e:
            print('Job failed', e)
