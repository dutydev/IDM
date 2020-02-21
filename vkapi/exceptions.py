class VkApiResponseException(Exception):
    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.get('error_code', None)
        self.error_msg = kwargs.get('error_msg', None)
        self.request_params = kwargs.get('request_params', None)


        self.args = args
        self.kwargs = kwargs

        
class InvalidMethodException(Exception):    
    def __init__(self, *args, **kwargs):
        self.method = list(args)[0]
        self.args = args
        self.kwargs = kwargs