# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from flask import jsonify, make_response


class RestAPIError():
    # def __init__(self, status_code=500, payload=None):
    #     print("hey2")
    #     self.status_code = status_code
    #     self.payload = payload

    def bad_input():
        return make_response(jsonify({ "code" : 400, "message": "Input Error: The service only supports png or jpg or jpeg images."}), 400)
    def bad_request():
        return make_response(jsonify({ "code" : 400, "message": "Input Error: Please check your key or value."}), 400)
    def word_limit():
        return make_response(jsonify({ "code" : 400, "message": "Input Error: Word Count Exceeded!"}), 400)
    def internal_server_error():
        return make_response(jsonify({ "code" : 500, "message": "Something went Wrong!"}), 500)
    
    

# class BadRequestError(RestAPIError):
#     def __init__(self, payload=None):
#         super().__init__(400, payload)


# class InternalServerErrorError(RestAPIError):
#     def __init__(self, payload=None):
#         super().__init__(500, payload)
