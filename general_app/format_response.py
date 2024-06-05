# Method for formatting validation error response to our need
def format_validation_error(errors):
    formatted_errors = []
    for field, field_errors in errors.items():
        error_dict = {field: field_errors}
        formatted_errors.append(error_dict)
    return {
        "message": "Validation Error",
        "errors": formatted_errors,
        "status_code": 400,
        "success": False,
    }


# Method for formatting error data which are not validation errors
def format_error_data(message, errors, status_code):
    return {
        "message": message,
        "errors": errors,
        "status_code": status_code,
        "success": False,
    }


# Method for formatting response data
def format_response_data(message, data, status_code):
    return {
        "message": message,
        "data": data,
        "status_code": status_code,
        "success": True,
    }
