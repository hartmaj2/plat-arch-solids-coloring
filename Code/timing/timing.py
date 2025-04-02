import time

HEADER = "TIMING:"
UNDERLINE_MARKER = "-"

# *tup packs the tuple of non-keyworded arguments into a tuple and names it `tup`
# **dic pack the tuple of keyworded arguments into a dict and names it `dic`
def run_timed(func, *args, **kwargs):
    start = time.time()
    res = func(*args, **kwargs) # * unpacs the tuple and ** unpacs the dict
    function = func.__name__
    end = time.time()
    duration = end - start
    print(HEADER)
    print("".join([UNDERLINE_MARKER for letter in HEADER]))
    print(f"{function=}\n{duration=}")
    return res
    