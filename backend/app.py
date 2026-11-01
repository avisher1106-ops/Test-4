import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from config import Config
from database import init_db, insert_log
from fruityvice_client import FruityviceError
from routes import router

logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def build_route(request: Request) -> str:
    route = request.url.path
    if request.url.query:
        route = f"{route}?{request.url.query}"
    return route


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except Exception as exc:
        logger.exception("Database initialisation failed")
        raise RuntimeError(
            f"Failed to initialise database '{Config.DB_NAME}': {exc}"
        ) from exc
    logger.info("Database '%s' is ready", Config.DB_NAME)
    yield


app = FastAPI(
    title="Fruity API",
    description=(
        "REST API that serves fruit data from https://www.fruityvice.com "
        "and logs every request to the MySQL table logs_db.logs."
    ),
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Fruits",
            "description": "Fruit data powered by the Fruityvice API",
        }
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    if not request.url.path.startswith("/api/"):
        return response

    try:
        await run_in_threadpool(
            insert_log,
            method=request.method,
            route=build_route(request),
            total_results=getattr(request.state, "total_results", 0),
            client_ip=get_client_ip(request),
        )
    except Exception as exc:
        logger.exception("Failed to save request log")
        error_response = JSONResponse(
            status_code=500,
            content={
                "error": "Failed to save request log",
                "details": str(exc),
            },
        )
        error_response.headers["Access-Control-Allow-Origin"] = "*"
        return error_response

    return response


@app.exception_handler(FruityviceError)
async def handle_fruityvice_error(request: Request, exc: FruityviceError):
    return JSONResponse(
        status_code=502,
        content={
            "error": "Failed to fetch data from the Fruityvice API",
            "details": str(exc),
        },
    )


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
