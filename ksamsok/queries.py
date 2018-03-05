import re

import requests

from .utils import valid_http_status

def bounding_box(auth, west, south, east, north, batch_size=50):
    raise NotImplementedError

def query(auth, query, batch_size=50):
    raise NotImplementedError

def text(auth, text, images=False, batch_size=50):
    raise NotImplementedError

def period(auth, start_time, end_time, batch_size=50):
    raise NotImplementedError

# not a generator
def hints(auth, text, count=5):
    request_query = auth.endpoint + 'ksamsok/api?x-api=' + auth.key + '&method=searchHelp&index=itemMotiveWord|eventName|itemKeyWord&prefix=' + text + '*&maxValueCount=' + str(count)

    r = requests.get(request_query)
    if not valid_http_status(r.status_code):
        return False

    terms_pattern = re.compile(r'<term>((?:.|\n)+?)<\/term>')
    value_pattern = re.compile(r'<value>(.+?)<\/value>')
    count_pattern = re.compile(r'<count>(\d+)<\/count>')

    result = list()
    for term in re.finditer(terms_pattern, r.text):
        print(term)
        parsed_term = {}

        parsed_term['value'] = value_pattern.search(term.group(1)).group(1)
        parsed_term['count'] = count_pattern.search(term.group(1)).group(1)

        result.append(parsed_term)

    return result

