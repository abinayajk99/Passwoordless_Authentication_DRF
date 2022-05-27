from rest_framework.response import Response


class GenericResponse(Response):
    def __init__(
        self,
        data={},
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        error_msg={},
        success_msg="",
        code="",
    ):
        super(Response, self).__init__(None, status=status)

        response_data = {
            "code": code,
            "success_message": success_msg,
            "error_message": error_msg,
            "payload": data,
        }

        return super(GenericResponse, self).__init__(
            response_data, status, template_name, headers, exception, content_type
        )
