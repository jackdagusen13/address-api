class RowNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AddressNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
