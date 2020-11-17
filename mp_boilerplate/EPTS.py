import multiprocessing as mp
import progressbar as pb
import typing as t
from threading import Thread
from typeguard import typechecked
from .core.MultiWorker import MultiWorker

class EPTS:
    
    @typechecked
    def __init__(
        self,
        extract: t.Callable[..., t.Iterator], transform: t.Callable[..., t.Any], save: t.Callable[..., None],
        transform_init: t.Callable[..., t.Any] = None,
        extract_args: t.Union[tuple, t.Any] = (), transform_init_args: t.Union[tuple, t.Any] = (), save_args: t.Union[tuple, t.Any] = (),
        worker_count: int =  mp.cpu_count(), show_progress: bool = False):
        """
        Sets up the (E)xtract (P)arallel (T)ransform (S)ave use case

        Parameters
        ----------
        extract : callable
            Function that creates items to process in the form `def extract(*args) -> iterator`
        transform : callable
            Function that processes items in the form `def transform(item) -> item` or `def transform(state, item) -> item`
        save : callable
            Function that saves processed items in the form `def save(iterator, *args) -> none`.
            Per PEP 484, there is no support for some, but not all of the function arguments to be typed.
        transform_init : callable
            Function for creating shared state in the background workers in the form `def transform_init(*args) -> item`
        extract_args : tuple
            The `*args` for `def extract(...)`
        transform_init_args : tuple
            The `*args` for `def transform_init(...)`
        save_args : tuple
            The `*args` for `def save(...)`
        worker_count : int
            How many background workers are supported for the 'P' part of 'EPTS'
        show_progress : bool
            Should a progress bar be displayed as part of `def save(...)`
        """
        assert extract is not None
        assert transform is not None
        assert save is not None
        assert extract_args is not None
        assert transform_init_args is not None
        assert save_args is not None
        assert worker_count > 0
        
        self._transform = MultiWorker(transform, transform_init, transform_init_args, worker_count)
        self._extract = Thread(target = EPTS._extract_wrapper, args = (self._transform, extract, extract_args))
        self._save = Thread(target = EPTS._save_wrapper, args = (self._transform, save, save_args, show_progress))

    @staticmethod
    def _extract_wrapper(worker: MultiWorker, fn: callable, args: tuple) -> None:
        iterator = fn() if len(args) == 0 else fn(*args)
        for item in iterator:
            worker.add_task(item)
        worker.finished_adding_tasks()

    @staticmethod
    def _save_wrapper(worker: MultiWorker, fn: callable, args: tuple, show_progress: bool) -> None:
        res1 = worker.get_results()
        res2 = res1 if not show_progress else EPTS._progress(res1)
        if len(args) == 0:
            fn(res2)
        else:
            fn(res2, *args)

    @staticmethod
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
        """
        Starts the use case
        """
        self._extract.start()
        self._transform.start()
        self._save.start()

    @typechecked
    def join(self) -> None:
        """
        Waits for all the items to be processed through the use case
        """
        self._extract.join()
        self._save.join()
