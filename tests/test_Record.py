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

def test_not_able_to_parse_error():
    pass

def test_parse_meta_data():
    record = Record.from_file('tests/resources/record_with_meta_only.rdf')

    assert record.meta['build_date'] == '2018-02-27'
    assert record.meta['created_date'] == '2018-02-27'
    assert record.meta['last_changed_date'] == '2017-06-28'
    assert record.meta['service'] == 'object'
    assert record.meta['service_org'] == 'MILI'
    assert record.meta['soch_version'] == '1.1'

def test_parse_core_values():
    record = Record.from_file('')

    assert record.uri == ''
    assert record.url == ''
    assert record.museumdat == ''
    assert record.thumbnail == ''
    assert record.super_type == ''
    assert record.type == ''
    assert record.label == ''

def test_parse_iterative_values():
    pass

def test_parse_empty_iterative_values():
    pass

def test_all_empty_except_uri():
    pass
