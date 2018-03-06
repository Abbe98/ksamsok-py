import pytest

from ksamsok import Record

def test_from_string():
    # we are only testing that the string results in a Record instance with 'raw_rdf' attribute
    # the fact that it's invalid should be tested by the parser.
    test_string = '<?xml version="1.0" encoding="UTF-8"?><rdf:RDF>dummy</rdf:RDF>'

    record = Record.from_string(test_string)
    assert record.raw_rdf == test_string

def test_from_file():
    record = Record.from_file('tests/resources/KBGF051559.rdf')

    assert record.raw_rdf.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert record.raw_rdf.endswith('</rdf:RDF>')

@pytest.mark.online
def test_from_uri():
    record = Record.from_uri('http://kulturarvsdata.se/raa/bbrm/21200000000487')

    assert record.raw_rdf.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert record.raw_rdf.endswith('</rdf:RDF>')
