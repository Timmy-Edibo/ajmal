import time
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from helpers import (generate_content, write_lines_batched_func, 
                     write_lines_using_asyncio_func, 
                     write_lines_using_threads_func,
                       write_to_file)

app = FastAPI(title="FastAPI app simulating delay to show performance of different optimzations")

@app.get("/")
def redirect():
    return RedirectResponse(url="/docs")


# Route for writing lines using normal threading with background task
@app.get("/synchronous-write")
def write_lines_threads_route():
    start_time = time.time()

    contents = [generate_content(i) for i in range(1, 20)]
    write_to_file("synchronous_write.txt", "".join(contents))
    end_time = time.time()

    print(f"write_lines_using_asyncio_func took {end_time - start_time:.4f} seconds")
    return {"message": "Lines will be written only"}


# Route for writing lines using normal threading with background task
@app.get("/write-lines-threads")
def write_lines_threads_route():
    write_lines_using_threads_func()
    return {"message": "Lines will be written using threads"}


# Route for writing lines using asyncio with background task
@app.get("/write-lines-asyncio")
async def write_lines_asyncio_route():
    await write_lines_using_asyncio_func()
    return {"message": "Lines will be written using asyncio"}


# Route for writing lines batched with asyncio
@app.get("/write-lines-batched")
def write_lines_batched_route():
    write_lines_batched_func()
    return {"message": "Lines will be written batched with asyncio"}
