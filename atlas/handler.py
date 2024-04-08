from flask import request, make_response


class EndpointHandler:
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        # request.view_args will be None if an exception occurred
        response = self.action(*args, **request.view_args)
        return make_response(response)
