from fastapi import FastAPI, Request
import time


def configurar_time_header(app: FastAPI):

    @app.middleware("http")
    async def time_header(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f} s"

        return response
