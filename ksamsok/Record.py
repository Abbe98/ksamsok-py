class Record:
    def __init__(self, record):
        pass

    def record_from_file(self, record):
        raise NotImplementedError

    def record_from_tree(self, record):
        raise NotImplementedError

    def record_from_uri(self, record):
        raise NotImplementedError

    def parse_record(self, tree):
        raise NotImplementedError

    def record_exists(self):
        raise NotImplementedError
