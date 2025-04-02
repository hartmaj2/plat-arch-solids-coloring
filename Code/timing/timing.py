import time

# run the function with the given non-keyword and keyword arguments and return the result and the run time as well
def run_and_get_time(func, *args, **kwargs):
    start = time.time()
    res = func(*args,**kwargs)
    return res, time.time() - start