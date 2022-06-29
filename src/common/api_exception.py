from builtins import Exception


class ApiException(Exception):
    def __init__(self, error: str, method_name=None):
        Exception.__init__(self, str, method_name)
        self.error = error
        self.method_name = method_name

    def __str__(self):
        if self.method_name:
            return f"Fatal exception occurred in the {self.method_name} method of the API Lambda: {self.error}"
        else:
            return f"Fatal exception occurred in the API Lambda: {self.error}"
