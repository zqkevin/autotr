
class RestApiRequest(object):

    def __init__(self):
        self.method = ""
        self.url = ""
        self.host = ""
        self.post_body = ""
        self.header = dict()
        self.json_parser = None
        self.header.update({"client_SDK_Version": "scrip.binance_futures-0.0.1-py3.9"})

