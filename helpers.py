import asyncio
import anyio
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool


# def generate_content(line_number):
#     return f"Line {line_number}\n"


def generate_content(line_number):
    # Simulating a time-consuming operation
    time.sleep(0.01)
    return f"Line {line_number}\n"


def write_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)


async def async_write_to_file(filename, content):
    await anyio.to_thread.run_sync(write_to_file, filename, content)

async def batch_async_write_to_file(filename, contents):
    await anyio.to_thread.run_sync(write_to_file, filename, ''.join(contents))

async def write_lines_using_asyncio_func():
    start_time = time.time()

    tasks = [async_write_to_file("output_asyncio.txt", generate_content(i)) for i in range(1, 20)]
    await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"write_lines_using_asyncio_func took {end_time - start_time:.4f} seconds")

def write_lines_using_threads_func():
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        contents = [generate_content(i) for i in range(1, 20)]
        futures = [executor.submit(write_to_file, "output_thread.txt", content) for content in contents]
        for future in futures:
            future.result()

    end_time = time.time()
    print(f"write_lines_using_threads_func took {end_time - start_time:.4f} seconds")

def write_lines_batched_func():
    start_time = time.time()

    contents = [generate_content(i) for i in range(1, 20)]
    chunk_size = 1000

    for i in range(0, len(contents), chunk_size):
        chunk = contents[i:i+chunk_size]
        asyncio.run(batch_async_write_to_file("output_batched.txt", chunk))

    end_time = time.time()
    print(f"write_lines_batched_func took {end_time - start_time:.4f} seconds")

