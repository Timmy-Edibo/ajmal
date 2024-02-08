import asyncio
import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


async def custom_middleware(request: Request, next_call):
    # Perform some tasks before the main application logic
    print("Middleware processing before the main logic")

    if request.url.path.startswith("/async"):
        await write_lines_batched_func__()

        # Call the next middleware or the main application logic
    response = await next_call(request)

    print("Middleware processing after the main logic")

    return response

# Apply the middleware to the FastAPI app
app.add_middleware(BaseHTTPMiddleware, dispatch=custom_middleware)

def generate_content(i):
    return f"Content {i}\n"

async def batch_async_write_to_file(filename, contents):
    await asyncio.to_thread(batch_sync_write_to_file, filename, contents)

def batch_sync_write_to_file(filename, contents):
    with open(filename, 'a') as file:
        file.write(''.join(contents))

async def write_lines_batched_func__():
    start_time = time.time()

    contents = [generate_content(i) for i in range(1, 100000)]
    chunk_size = 1000

    tasks = []
    for i in range(0, len(contents), chunk_size):
        chunk = contents[i:i+chunk_size]
        task = asyncio.create_task(batch_async_write_to_file("output_batched.txt", chunk))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"write_lines_batched_func took {end_time - start_time:.4f} seconds")

# Define a route
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/async")
async def read_root():
    return {"message": "Asyncing IO running!"}
