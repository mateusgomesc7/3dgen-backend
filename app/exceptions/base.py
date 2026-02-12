class AppDetailedError(Exception):
    """
    Base exception class for application-specific errors with detailed
    messages and codes.
    """

    def __init__(self, detail: str, code: str = 'INTERNAL_ERROR'):
        self.detail = detail
        self.code = code
        super().__init__(self.detail)


class NotFoundError(AppDetailedError):
    def __init__(self, detail: str = 'Resource not found'):
        super().__init__(detail=detail, code='NOT_FOUND')


class BadRequestError(AppDetailedError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, code='BAD_REQUEST')


class ConflictError(AppDetailedError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, code='CONFLICT')
