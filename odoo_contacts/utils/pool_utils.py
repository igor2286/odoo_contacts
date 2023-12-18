from collections.abc import Callable
from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import Iterable
import more_itertools


def _submit(call_func: Callable,
            workers: int,
            chunks: Iterable,
            return_result: bool,
            *args,
            **kwargs):
    """Util for execute multiprocessing"""
    result, errors = [], []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(call_func, chunk, *args, **kwargs) for chunk in chunks]
        # process task results as they are available
        for future in as_completed(futures):
            # retrieve the result
            if future.exception():
                print(future.exception())
                errors.append(future.exception())
            if return_result:
                result.extend(future.result())

    if errors:
        with open('errors_log.txt', 'w') as file:
            file.writelines(errors)

    if return_result:
        return result


def process_polling(
        call_func: Callable,
        iterable: Iterable,
        workers: int = int(cpu_count() / 2),
        return_result: bool = True,
        *args,
        **kwargs):
    """Util for setup multiprocessing"""
    if workers > len(iterable):
        workers = len(iterable)

    chunks = more_itertools.divide(workers, iterable)

    result = _submit(call_func=call_func,
                     workers=workers,
                     chunks=chunks,
                     return_result=return_result,
                     *args,
                     **kwargs)

    if return_result:
        return result
