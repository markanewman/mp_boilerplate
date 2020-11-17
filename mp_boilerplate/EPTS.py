import multiprocessing as mp
import progressbar as pb
import typing as t
from threading import Thread
from typeguard import typechecked
from .core.MultiWorker import MultiWorker

class EPTS:
    
    @typechecked
    def __init__(self, \
        extract: callable, transform: callable, save: callable, \
        transform_init: t.Optional[callable] = None, extract_args: t.Optional[tuple] = None, transform_init_args: t.Optional[tuple] = None, save_args: t.Optional[tuple] = None, \
        worker_count: int =  mp.cpu_count(), show_progress: bool = False):
        assert extract is not None
        assert transform is not None
        assert save is not None
        
        self._transform = MultiWorker(transform, transform_init, transform_init_args, worker_count)
        self._extract = Thread(target = EPTS._extract_wrapper, args = (self._transform, extract, extract_args))
        self._save = Thread(target = EPTS._save_wrapper, args = (self._transform, save, save_args, show_progress))

    @staticmethod
    @typechecked
    def _extract_wrapper(worker: MultiWorker, fn: callable, args: t.Optional[tuple]) -> None:
        iterator = fn() if args is None else fn(args)
        for item in iterator:
            worker.add_task(item)
        worker.finished_adding_tasks()

    @staticmethod
    @typechecked
    def _save_wrapper(worker: MultiWorker, fn: callable, args: t.Optional[tuple], show_progress: bool) -> None:
        res1 = worker.get_results()
        res2 = res1 if not show_progress else EPTS._progress(res1)
        args = (res2) if args is None else (res2) + list(args) 
        fn(args)

    @staticmethod
    @typechecked
    def _progress(items: t.Iterator) -> t.Iterator:
        bar_i = 0
        widgets = [ 'Saving Items # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
        with pb.ProgressBar(widgets = widgets) as bar:
            for item in items:
                bar_i = bar_i + 1
                bar.update(bar_i)
                yield item

    @typechecked
    def start(self) -> None:
        self._extract.start()
        self._transform.start()
        self._save.start()

    @typechecked
    def join(self) -> None:
        self._extract.join()
        self._save.join()
