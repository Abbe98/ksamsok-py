# KSamsök-PY

KSamsök-PY is a Python library for the [K-Samsök(SOCH) API](http://www.ksamsok.se/in-english/). The K-Samsök aggregator has over 6.8 million cultural objects indexed from various sources.

## Documentation

### Install

```bash
pip install ksamsok
```

### Usage

#### Initialization

**Importing**

```python
from ksamsok import KSamsok
```

Many action within the API requires an API key that you can obtain by contacting the Swedish National Heritage Board. For development you can use the key `test`.

For using this library against custom Kulturarvsdata / K-Samsök endpoints see a section at the end of this document.

Example without an API key:

```python
culturalSerach = KSamsok()
```

Example with an API key:

```python
culturalSerach = KSamsok('test')
```

#### Text Search

Requires an API key.

The basic `search()` method has a total of four parameters:

 - text(`string`), the string to search for in K-Samsök.
 - start(`int`), the result to start at, for returning the first result this should be set to 1.
 - hits(`int`), the number of results to return(1-500 is valid).
 - image(`boal`), optional parameter, set to true if you only want to return objects with images.

```python
# search for "kyrka" starting at the first result returning the next 10 results
culturalSerach.search('kyrka', 0, 10)
```

```python
# search for "kyrka" starting at the first result returning the next 10 results but only include results with images
culturalSerach.search('kyrka', 0, 10, true)
```

#### Bounding Box Search

Requires an API key.

The method `geoSearch()` allows you to search by a geographical bounding box. `geoSearch()` has six parameters:

 - west(`int`), the most west longitude border of your bounding box.
 - south(`int`), the most south latitude border of your bounding box.
 - east(`int`), the most east longitude border of your bounding box.
 - north(`int`), the most north latitude border of your bounding box.
 - start(`int`), the result to start at, for returning the first result this should be set to 1.
 - hits(`int`), optional by default set to 60. The number of results to return (1-500).

```python
# Search within bonding box(west, south, east, north) starting at result 300 returning 500 results
culturalSerach.geoSearch(16.41, 59.07, 16.42, 59.08, 300, 500)
```

#### URI Format

The `formatUri()` method can validate and convert SOCH URI/URL;s. `formatUri()` will return `False` if provided with a invalid URI. `formatUri()` has three parameters:

 - uri(`string`), the URI or URL to the object.
 - format(`string`), All supported output/input formats:
  - `raw`(default)
  - `rawurl`
  - `xml`
  - `xmlurl`
  - `jsonld`
  - `jsonldurl`
  - `rdf`
  - `rdfurl`
  - `html`
  - `htmlurl`
  - `museumdat`
  - `museumdaturl`
 - validate(`bool`), optional, if set to `True` it check if an object for the URI exists.

```python
# get the HTML-link version of the following URI
culturalSerach.formatUri('raa/kmb/16001000540365', 'htmlurl')
```

```python
# get the XML resource URI
culturalSerach.formatUri('raa/kmb/16001000540365', 'xml')
```

```python
# validate the URI(returns the requested format if valid otherwise False)
culturalSerach.formatUri('raa/kmb/16001000540365', 'rdf', True)
```

#### Relations

Requires an API key.

The `getRelations()` method allows you to return a list of object related to another. The method has only one parameter:

 - object uri(`string`), an valid URI for a object in K-Samsök. The parameters allows different types of URIs described below.

Raw URLs/URIs such as:

 - `http://kulturarvsdata.se/raa/kmb/16000300020896`
 - `raa/fmi/10028201230001`

HTML, JSONLD, RDF, XML, MuseumDAT resource URLs/URIs:

 - `http://kulturarvsdata.se/raa/kmb/xml/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/rdf/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/html/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/jsonld/16000300020896`
 - `raa/kmb/xml/16000300020896`
 - `raa/kmb/rdf/16000300020896`
 - `raa/kmb/html/16000300020896`
 - `raa/kmb/jsonld/16000300020896`

```python
# get all relations from URI
culturalSerach.getRelations('raa/fmi/10028201230001')
```

#### Object

The `getObject()` method returns a object based on a URI or URL. The method has only one parameter:

 - object uri(`string`), a valid URI for a object in K-Samsök. The parameters allows different types of URIs described below.

Raw URLs/URIs such as:

 - `http://kulturarvsdata.se/raa/kmb/16000300020896`
 - `raa/fmi/10028201230001`

HTML, JSONLD, RDF, XML resource URLs/URIs:

 - `http://kulturarvsdata.se/raa/kmb/xml/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/rdf/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/html/16000300020896`
 - `http://kulturarvsdata.se/raa/kmb/jsonld/16000300020896`
 - `raa/kmb/xml/16000300020896`
 - `raa/kmb/rdf/16000300020896`
 - `raa/kmb/html/16000300020896`
 - `raa/kmb/jsonld/16000300020896`

```python
# get single object (record)
culturalSerach.getObject('raa/fmi/10028201230001')
```

#### Search Hints

Requires an API key.

The `getHints()` method allows you to return search suggestions from a string. This method has two parameters:

 - text(`string`), the string to get suggestions from.
 - hits(`int`), optional the number of suggestions to return, 5 by default.

```python
# get a search hint for the string "na"
culturalSerach.getHints('na')
```

### Advanced Usage: Extending

When KSamsök-PY does not have a method for a request you want to preform against the K-Samsök API extending KSamsök-PY might be the solution. Extending KSamsök-PY allows you to use KSamsök-PY methods for formating URIs, validate responds, parsing and more while defining your own API queries.

**Note that this may require that you are familiar with The K-Samsök(SOCH) API and object oriented Python**

There are two `protected` methods that essential when extending `KSamsok`, `killXmlNamespaces()` and `parseRecord()` those are the same functions as `public` methods uses.

To get started with see the [implementation of `search()`](https://github.com/Abbe98/ksamsok-py/blob/master/ksamsok/ksamsok.py#L179). Note that `KSamsok` parses and uses the "XML Presentation" format and not the RDF format provided by SOCH.

### Advanced Usage: Custom Endpoint

You can setup ksamsok-py to work against a custom Kulturarvsdata / K-Samsök instance by passing in an `endpoint` parameter to the constructor:

```python
culturalSerach = KSamsok(key='test', endpoint='https://example.com/')
```

Note that when using an custom endpoint `formatUri()` will still output URLs targeting kulturarvsdata.se and not the custom endpoint. It will accept custom URIs as input.
