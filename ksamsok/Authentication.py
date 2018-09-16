from .utils import validate_request

class Authentication:
    def __init__(self, key, endpoint='http://kulturarvsdata.se/'):
        self.endpoint = endpoint
        self.key = key

        if self.key:
            test_query = self.endpoint + 'ksamsok/api?x-api=' + key + '&method=search&query=text%3D"test"&recordSchema=presentation'

            if not validate_request(test_query):
                raise ValueError('Bad API key or inaccessible endpoint.')

    def __repr__(self):
        return '{0} {1}'.format(self.__class__, self.__dict__)
