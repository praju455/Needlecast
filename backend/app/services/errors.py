"""Define safe service failures that cross the M00 HTTP boundary."""

from backend.app.schemas.api import Error


class ServiceError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


ERROR_RESPONSES = {
    404: {"model": Error, "description": "The requested sample resource is unavailable."},
    409: {"model": Error, "description": "The retry key belongs to a different request."},
    422: {"model": Error, "description": "The request did not match the placeholder contract."},
    503: {"model": Error, "description": "Required assets or the selected mode are unavailable."},
}
