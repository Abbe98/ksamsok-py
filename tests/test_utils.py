import pytest

from ksamsok import utils

# valid kulturarvsdata representations with the URI they should resolve to
valid_kulturarvsdata = [
    ['raa/fmi/10028201230001', 'http://kulturarvsdata.se/raa/fmi/10028201230001'],
    ['shm/site/18797', 'http://kulturarvsdata.se/shm/site/18797'],
    ['raa/kmb/xml/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['raa/kmb/rdf/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['raa/kmb/html/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['raa/kmb/jsonld/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['raa/kmb/museumdat/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/xml/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/rdf/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/html/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/jsonld/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
    ['http://kulturarvsdata.se/raa/kmb/museumdat/16000300020896', 'http://kulturarvsdata.se/raa/kmb/16000300020896'],
]

invalid_kulturarvsdata = [
    'kulturarvsdata.se/raa/kmb/16000300020896',
    'rdf/16000300020896',
    'http://kulturarvsdata.se/raa/kmb/',
    'raa/kmb/xml/',
    ''
]

def test_kringla_to_uri_basic():
    kringla_url = 'http://www.kringla.nu/kringla/objekt?referens=SMVK-MM/video/4279090'
    assert utils.kringla_to_uri(kringla_url) == 'http://kulturarvsdata.se/SMVK-MM/video/4279090'

def test_kringla_to_uri_with_query_string():
    kringla_url = 'http://www.kringla.nu/kringla/objekt?filter=filter=itemType%3Dobjekt/föremål&referens=shm/object/398394'
    assert utils.kringla_to_uri(kringla_url) == 'http://kulturarvsdata.se/shm/object/398394'

def test_kringla_to_uri_invalid():
    kringla_url = 'http://www.kringla.nu/kringla/sok?text=Ingen+uppgift&filter=thumbnailExists%3Dj&filter=itemType%3Dfoto&antal=2'
    assert not utils.kringla_to_uri(kringla_url)

def test_kulturarvsdata_to_uri():
    for item in valid_kulturarvsdata:
        assert utils.kulturarvsdata_to_uri(item[0]) == item[1]

def test_kulturarvsdata_to_uri_invalids():
    for item in invalid_kulturarvsdata:
        assert not utils.kulturarvsdata_to_uri(item)

def test_kulturarvsdata_to_id():
    for item in valid_kulturarvsdata:
        # URI - http://kulturarvsdata.se/ (25 characters)
        assert utils.kulturarvsdata_to_id(item[0]) == item[1][25:]

def test_kulturarvsdata_to_id_invalids():
    for item in invalid_kulturarvsdata:
        assert not utils.kulturarvsdata_to_id(item)
