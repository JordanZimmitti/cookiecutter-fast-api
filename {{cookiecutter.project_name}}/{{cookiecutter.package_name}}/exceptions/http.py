from fastapi import HTTPException, status


class BadRequestError(HTTPException):
    def __init__(self, message: str):
        """
        Error class that is raised when a client has sent a request
        that is malformed or with incorrect data

        :param message: The message sent back to the client detailing the problem
        """
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class ForbiddenError(HTTPException):
    def __init__(self, message: str):
        """
        Error class that is raised when a client is authenticated but
        is not authorized to access a specific route

        :param message: The message sent back to the client detailing the problem
        """
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class InternalServerError(HTTPException):
    def __init__(self, message: str = "An unexpected error occurred, please try again"):
        """
        Error class that is raised when an unrecoverable
        server error occurs

        :param message: The message sent back to the client detailing the problem
        """
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


class NotFoundError(HTTPException):
    def __init__(self, message: str):
        """
        Error class that is raised when a client is trying to
        access an endpoint or resource that does not exist

        :param message: The message sent back to the client detailing the problem
        """
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UnauthenticatedError(HTTPException):
    def __init__(self, message: str):
        """
        Error class that is raised when an untrusted client
        is trying to access an endpoint

        :param message: The message sent back to the client detailing the problem
        """
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)
