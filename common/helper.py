import os
import re
import time
from functools import wraps


def get_project_path():
    helper_path = os.path.abspath(__file__)
    common_path = os.path.dirname(helper_path)
    project_path = os.path.dirname(common_path)
    return project_path


def escape_special_characters(name: str, replace_char: str = ''):
    escaped = ''.join(
        char if char.isalnum() or char == ' ' else replace_char
        for char in name
    )
    escaped = re.sub(' +', '_', escaped)
    return escaped


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
