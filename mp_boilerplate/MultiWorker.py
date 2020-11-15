import multiprocessing as mp
import typing as t
from threading import Thread
from typeguard import typechecked

class MultiWorker:

    _sentinel = None
    _finished_adding = False

    @typechecked
    def __init__(self, job: callable, init: callable = None, init_args: t.Optional[tuple] = None, worker_count: int = mp.cpu_count()) -> None:
        self._tasks = mp.Queue()
        self._results = mp.Queue()
        self._workers = []
        for _ in range(worker_count):
            self._workers.append(mp.Process(target = MultiWorker._worker, args = (job, init, init_args, self._tasks, self._results)))
        self._overlord = Thread(target = MultiWorker._overlord, args = (self._workers, self._tasks, self._results))

    @staticmethod
    @typechecked
    def _worker(job: callable, init: callable, init_args: t.Optional[tuple], tasks: mp.Queue, results: mp.Queue) -> None:
        state = None
        if init is not None:
            state = init(init_args)
        while True:
            item = tasks.get()
            if item == MultiWorker._sentinel:
                tasks.put(MultiWorker._sentinel)
                break            
            else:
                if state is None:
                    result = job(item)
                else:
                    result = job(state, item)
                results.put(result)

    @staticmethod
    @typechecked
    def _overlord(workers: t.List[mp.Process], tasks: mp.Queue, results: mp.Queue) -> None:
        for worker in workers:
            worker.join()
        results.put(MultiWorker._sentinel)
        tasks.close()

    @typechecked
    def start(self) -> None:
        for worker in self._workers:
            worker.start()
        self._overlord.start()
    
    @typechecked
    def add_task(self, item) -> None:
        self._tasks.put(item)

    @typechecked
    def finished_adding_tasks(self) -> None:
        if not self._finished_adding:
            self._finished_adding = True
            self._tasks.put(MultiWorker._sentinel)

    @typechecked
    def get_results(self) -> t.Iterator:
        while True:
            item = self._results.get()
            if item == MultiWorker._sentinel:
                break
            else:
                yield item
        self._results.close()

