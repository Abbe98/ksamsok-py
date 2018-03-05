import pytest

from ksamsok import Authentication

@pytest.mark.online
def test_init_authentication():
    # this test only expects the Authentication not to raise an exception
    auth = Authentication('test')

@pytest.mark.online
def test_bad_api_key():
    with pytest.raises(ValueError) as excinfo:
        auth = Authentication('hejsan-hoppsan-45fg')
    
    assert 'Bad API key or inaccessible endpoint.' in str(excinfo.value)

@pytest.mark.online
def test_bad_endpoint():
    with pytest.raises(ValueError) as excinfo:
        auth = Authentication('test', endpoint='http://example.com')
    
    assert 'Bad API key or inaccessible endpoint.' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        auth = Authentication('test', endpoint='not-even-an-URL')
    
    assert 'Bad API key or inaccessible endpoint.' in str(excinfo.value)
