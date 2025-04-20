import time
import multiprocessing
from collections.abc import Callable
from queue import Empty

# run the function with the given non-keyword and keyword arguments and return the result and the run time as well
def run_and_get_time(func, *args, **kwargs):
    start = time.time()
    res = func(*args,**kwargs)
    return res, time.time() - start

# for some reason this wrapper function needs to be defined outside of try_run_for_t_seconds2 function
def _wrapper_func(function, q, args):
    try:
        result = function(*args)
        q.put(('ok', result))
    except Exception as e:
        q.put(('error', e))

# function that waits for the result of function and returns it if the function finished in t_seconds seconds or terminates it and returns None
def try_run_for_t_seconds2(t_seconds: int, function: Callable, *args):
    with multiprocessing.Manager() as manager:
        result_queue = manager.Queue()
        p = multiprocessing.Process(target=_wrapper_func, args=(function, result_queue, args))
        p.start()
        p.join(timeout=t_seconds)

        if p.is_alive():
            p.terminate()
            p.join()
            return None

        try:
            status, value = result_queue.get_nowait()
            if status == 'ok':
                return value
            else:
                raise value
        except Empty:
            return None