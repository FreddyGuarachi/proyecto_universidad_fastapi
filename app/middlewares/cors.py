from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time


def configurar_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
