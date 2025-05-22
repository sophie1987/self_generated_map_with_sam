import time

def get_time(f):
    def inner(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f'{f.__name__} consume {"%.3f" %(end - start)} seconds')
        return result
    return inner