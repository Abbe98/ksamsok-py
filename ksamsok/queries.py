def bounding_box(auth, west, south, east, north, batch_size=50):
    raise NotImplementedError

def query(auth, query, batch_size=50):
    raise NotImplementedError

def text(auth, text, images=False, batch_size=50)
    raise NotImplementedError

def period(auth, start_time, end_time, batch_size=50)
    raise NotImplementedError

# not a generator
def hints(auth, text, count):
    raise NotImplementedError
