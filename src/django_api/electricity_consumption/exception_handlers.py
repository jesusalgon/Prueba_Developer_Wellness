from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 400:
            response.data['detail'] = 'Bad request'

        if response.status_code == 404:
            response.data['detail'] = 'Not found'

        if response.status_code == 500:
            response.data['detail'] = 'Internal Server Error'

        response.data['status_code'] = response.status_code

    return response