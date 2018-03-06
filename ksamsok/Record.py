import requests

from .utils import validate_request
from .utils import valid_http_status

class Record:
    raw_rdf = None

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as file:
            return cls(file.read())

    @classmethod
    def from_string(cls, record):
        return cls(record)

    @classmethod
    def from_uri(cls, uri):
        r = requests.get(uri)
        if not valid_http_status(r.status_code):
            #TODO better exception
            raise Exception('URI responded with http status code: ' + str(r.status_code))

        return cls(r.text)

    def __init__(self, record):
        self.raw_rdf = record
        self.parse()

    def parse(self, tree):
        raise NotImplementedError

    def exists(self):
        # should implement utils.validate_request but from local extracted URI
        raise NotImplementedError
