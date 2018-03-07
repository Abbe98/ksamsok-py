import pytest

from ksamsok import Record

def test_from_string():
    # we are only testing that the string results in a Record instance with 'raw_rdf' attribute
    # the fact that it's invalid should be tested by the parser.
    test_string = '<?xml version="1.0" encoding="UTF-8"?><rdf:RDF>dummy</rdf:RDF>'

    with pytest.raises(Exception) as excinfo:
        record = Record.from_string(test_string)
        assert record.raw_rdf == test_string

        assert 'Could not parse URI from given record.' in str(excinfo.value)

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
    with pytest.raises(Exception) as excinfo:
        record = Record.from_string('crap')
        assert 'Could not parse URI from given record.' in str(excinfo.value)

def test_parse_meta_data():
    record = Record.from_file('tests/resources/record_with_meta_only.rdf')

    assert record.meta['build_date'] == '2018-02-27'
    assert record.meta['created_date'] == '2018-02-27'
    assert record.meta['last_changed_date'] == '2017-06-28'
    assert record.meta['service'] == 'object'
    assert record.meta['service_org'] == 'MILI'
    assert record.meta['soch_version'] == '1.1'

def test_parse_core_values():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert record.uri == 'http://kulturarvsdata.se/inst/service/objekt-id'
    assert record.url == 'https://example.com/url'
    assert record.museumdat == 'https://example.com/museumdat'
    assert record.thumbnail == 'https://example.com/thumbnail.jpg'
    assert record.super_type == 'http://kulturarvsdata.se/resurser/EntitySuperType#specTyp'
    assert record.label == 'item label'
    assert record.type == 'http://kulturarvsdata.se/resurser/EntityType#specTyp'

def test_parse_iterative_values():
    pass

def test_parse_empty_iterative_values():
    pass

def test_all_empty_except_uri():
    pass
