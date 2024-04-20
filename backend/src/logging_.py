__all__ = ["logger", "socket_logger", "suspend_logging"]

import asyncio
import contextlib
import inspect
import logging.config
import os
from typing import Dict, Any

import fastapi
import yaml
from fastapi.dependencies.models import Dependant
from pymongo import monitoring
from starlette.concurrency import run_in_threadpool


class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        logger.debug(
            "Command {0.command_name} with request id " "{0.request_id} started on server " "{0.connection_id}".format(
                event
            )
        )

    def succeeded(self, event):
        logger.debug(
            "Command {0.command_name} with request id "
            "{0.request_id} on server {0.connection_id} "
            "succeeded in {0.duration_micros} "
            "microseconds".format(event)
        )

    def failed(self, event):
        logger.debug(
            "Command {0.command_name} with request id "
            "{0.request_id} on server {0.connection_id} "
            "failed in {0.duration_micros} "
            "microseconds".format(event)
        )


monitoring.register(CommandLogger())


class RelativePathFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.relativePath = os.path.relpath(record.pathname)
        return True


with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger("src")
logger.addFilter(RelativePathFilter())


class NoPingPongFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not ("Received packet PONG" in record.getMessage() or "Sending packet PING" in record.getMessage())


class NoTooLongInfoFilter(logging.Filter):
    def __init__(self, max_length: int):
        super().__init__()
        self.max_length = max_length

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno == logging.INFO and len(record.getMessage()) >= self.max_length:
            record.msg = record.getMessage()[: self.max_length - 3] + "..."
            record.args = None  # all args are included in the message already
        return True


socket_logger = logging.getLogger("socketio")
socket_logger.addFilter(NoPingPongFilter())
socket_logger.addFilter(NoTooLongInfoFilter(1000))


async def run_endpoint_function(*, dependant: Dependant, values: Dict[str, Any], is_coroutine: bool) -> Any:
    # Only called by get_request_handler. Has been split into its own function to
    # facilitate profiling endpoints, since inner functions are harder to profile.
    assert dependant.call is not None, "dependant.call must be a function"
    loop = asyncio.get_running_loop()
    start_time = loop.time()
    if is_coroutine:
        r = await dependant.call(**values)
    else:
        r = await run_in_threadpool(dependant.call, **values)
    finish_time = loop.time()
    duration = finish_time - start_time
    callback = dependant.call
    func_name = callback.__name__
    pathname = inspect.getsourcefile(callback) or "unknown"
    lineno = inspect.getsourcelines(callback)[1]
    record = logging.LogRecord(
        name="src.fastapi.run_endpoint_function",
        level=logging.INFO,
        pathname=pathname,
        lineno=lineno,
        msg=f"Handler `{func_name}` took {int(duration * 1000)} ms",
        args=(),
        exc_info=None,
        func=func_name,
    )
    record.relativePath = os.path.relpath(record.pathname)
    logger.handle(record)
    return r


# monkey patch fastapi to log endpoint function duration and link to source code
fastapi.routing.run_endpoint_function = run_endpoint_function


@contextlib.contextmanager
def suspend_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
