class ServiceUnavailableError(Exception):
    """When a required service/functionality is not available"""

    pass


class ResourceNotFoundError(Exception):
    """When a requested resource is not found"""

    pass


class TextRequiredError(Exception):
    """When text input is required but missing"""

    pass


class PhotoRequiredError(Exception):
    """When photo is required but missing"""

    pass


class PatternValidationError(Exception):
    """When input doesn't match required pattern"""

    pass


class IntegerValidationError(Exception):
    """When integer input is required"""

    pass


class DuplicateError(Exception):
    """When input is duplicate"""

    pass
