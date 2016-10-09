# KSamsök-PY

KSamsök-PHP is a PHP library for the [K-Samsök(SOCH) API](http://www.ksamsok.se/in-english/). The K-Samsök aggregator has over 6.3 million cultural objects indexed from various sources.

## Install

```
pip install ksamsok
```

## Usage

I have yet to write the future but amazing documentation for this library, sorry for that.

```python
from ksamsok import KSamsok

# init with your K-Samsök API key,
# an optional API parameter can be used for custom API endpoints
culturalSerach = KSamsok('test')

# search for "kyrka" starting at the first result returning the next 10 results
# a optional bool can be set to only include results that have an image
culturalSerach.search('kyrka', 0, 10)

# Search within bonding box(west, south, east, north) starting at result 300 returning 500 results
culturalSerach.geoSearch(16.41, 59.07, 16.42, 59.08, 300, 500)

# get the HTML-link version of the following URI
culturalSerach.formatUri('raa/kmb/16001000540365', 'htmlurl')

# get the XML resource URI
culturalSerach.formatUri('raa/kmb/16001000540365', 'xml')

# validate the URI(returns the requested format if valid otherwise False)
culturalSerach.formatUri('raa/kmb/16001000540365', 'rdf', True)

# for a full list of supported URI formats see:
# http://byabbe.se/ksamsok-php/#uri

# get all relations from URI
culturalSerach.getRelations('raa/fmi/10028201230001')

# get single object(record)
culturalSerach.getObject('raa/fmi/10028201230001')

# get a search hint for the string "na"
culturalSerach.getHints('na')
```

## Extending

You can add your own powerful extensions to KSamsok-PY by extending the class and take advantage of functions such as `parseRecord()`.
