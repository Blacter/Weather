class KeyError(Exception):
    def __init__(self, key_with_error: str, request_method: str):
        self.key_with_error = key_with_error
        self.request_method = request_method
        
    def __str__(self) -> str:
        return f'{self.request_method.upper()} KeyError: key {self.key_with_error} does not exists.'
