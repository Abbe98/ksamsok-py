import pytest

from ksamsok import Authentication
from ksamsok import queries

auth = Authentication('test')

@pytest.mark.online
def test_default_hints():
    hints = queries.hints(auth, 'fisk')

    assert len(hints) == 5

    for hint in hints:
        assert len(hint['value']) > 0
        assert hint['count'].isdigit()

@pytest.mark.online
def test_more_then_default_hints():
    hints = queries.hints(auth, 'glass', count=10)

    assert len(hints) > 5

@pytest.mark.online
def test_no_hints():
    hints = queries.hints(auth, 'random_stupid_string_hej')

    assert isinstance(hints, list)
