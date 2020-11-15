# mp_boilerplate

A collection of patterns to use over top of the built in multiprocessing package


```{py}
def process_int(i):
    return i + 1

worker = pat.MultiWorker(process_int)
worker.start()

for i in range(100):
    worker.add_task(i)
worker.finished_adding_tasks()

for item in worker.get_results():
    print(item)
```