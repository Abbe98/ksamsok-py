# KSamsök-PY

KSamsök-PY is a Python library for the [K-samsök(SOCH) API](http://www.ksamsok.se/in-english/). The K-samsök aggregator has over 7.5 million cultural objects indexed from various sources.

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

For using this library against custom Kulturarvsdata / K-samsök endpoints see a section at the end of this document.

```python
culturalSearch = KSamsok()
```

#### Text Search

The basic `search()` method has a total of four parameters:

 - text(`string`), the string to search for in K-Samsök.
 - start(`int`), the result to start at, for returning the first result this should be set to 1.
 - hits(`int`), the number of results to return(1-500 is valid).
 - image(`bool`), optional parameter, set to true if you only want to return objects with images.

```python
# search for "kyrka" starting at the first result returning the next 10 results
culturalSearch.search('kyrka', 0, 10)
```

```python
# search for "kyrka" starting at the first result returning the next 10 results but only include results with images
culturalSearch.search('kyrka', 0, 10, true)
```

#### Bounding Box Search

The method `geoSearch()` allows you to search by a geographical bounding box. `geoSearch()` has six parameters:

 - west(`int`), the most west longitude border of your bounding box.
 - south(`int`), the most south latitude border of your bounding box.
 - east(`int`), the most east longitude border of your bounding box.
 - north(`int`), the most north latitude border of your bounding box.
 - start(`int`), the result to start at, for returning the first result this should be set to 1.
 - hits(`int`), optional by default set to 60. The number of results to return (1-500).

```python
# Search within bonding box(west, south, east, north) starting at result 300 returning 500 results
culturalSearch.geoSearch(16.41, 59.07, 16.42, 59.08, 300, 500)
```

#### CQL Queries

The method `cql()`

 - query(`string`), the query string for K-samsök.
 - start(`int`), the result to start at, for returning the first result this should be set to 1.
 - hits(`int`), optional by default set to 60. The number of results to return (1-500).

```python
# Search for photos with coordinates and images.
culturalSearch.cql('geoDataExists=n AND thumbnailExists=j AND itemType=foto', 0)
```

#### CQL Queries Genertor

The generator `cqlGenerator()` takes only one parameter and allows you to loop through the results:

 - query(`string`), the query string to for K-samsök.

```python
# Search for photos with coordinates and images.
for item in culturalSearch.cql('geoDataExists=n AND thumbnailExists=j AND itemType=foto'):
    print(item)
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
culturalSearch.formatUri('raa/kmb/16001000540365', 'htmlurl')
```

```python
# get the XML resource URI
culturalSearch.formatUri('raa/kmb/16001000540365', 'xml')
```

```python
# validate the URI(returns the requested format if valid otherwise False)
culturalSearch.formatUri('raa/kmb/16001000540365', 'rdf', True)
```

#### Kringla to URI

The `kringlaToUri()` method can convert Kringla.nu item URLs to Kulturarvsdata URIds similar to `formatUri()`. `kringlaToUri()` will return `False` if it's given a invalid Kringla.nu item URL.

 - kringla(`string`), the URL to the item at Kringla.nu.
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
# get the full kulturarvsdata URL from a basic Kringla item link.
culturalSearch.kringlaToUri('http://www.kringla.nu/kringla/objekt?referens=raa/fmi/10253101370001', 'rawurl')
```

```python
# get the RDF resource id from a Kringla link with search parameters
culturalSearch.kringlaToUri('http://www.kringla.nu/kringla/objekt?filter=itemType%3Dfoto&referens=DFH/media/DFH_DFH00574', 'rdf')
```

#### Relations

The `getRelations()` method allows you to return a list of objects related to another. The method has only one parameter:

 - object uri(`string`), a valid URI for an object in K-samsök. The parameters allows different types of URIs described below.
 - infer same as (`bool`), decides relations are inferred from owl:sameAs statements, defaults to false.

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
# get all relations from a URI
culturalSearch.getRelations('raa/fmi/10028201230001')
```

```python
# get all relations from a URI and other URIs with owl:sameAs pointing to the given one
culturalSearch.getRelations('raa/fmi/10028201230001', infer_same_as=True)
```

#### Object

The `getObject()` method returns an object based on a URI or URL. The method has only one parameter:

 - object uri(`string`), a valid URI for an object in K-samsök. The parameters allows different types of URIs described below.

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
culturalSearch.getObject('raa/fmi/10028201230001')
```

#### Search Hints

The `getHints()` method allows you to return search suggestions from a string. This method has two parameters:

 - text(`string`), the string to get suggestions from.
 - hits(`int`), optional the number of suggestions to return, 5 by default.

```python
# get a search hint for the string "na"
culturalSearch.getHints('na')
```

### Advanced Usage: Extending

When KSamsök-PY does not have a method for a request you want to preform against the K-samsök API extending KSamsök-PY might be the solution. Extending KSamsök-PY allows you to use KSamsök-PY methods for formating URIs, validate responds, parsing and more while defining your own API queries.

**Note that this may require that you are familiar with The K-samsök(SOCH) API**

There are two `protected` methods that essential when extending `KSamsok`, `killXmlNamespaces()` and `parseRecord()` those are the same functions as `public` methods uses.

To get started with see the [implementation of `cql()`](https://github.com/Abbe98/ksamsok-py/blob/master/ksamsok/ksamsok.py#L220). Note that `KSamsok` parses and uses the "XML Presentation" format and not the RDF format provided by SOCH.

### Advanced Usage: Custom Endpoint

You can setup ksamsok-py to work against a custom Kulturarvsdata / K-samsök instance by passing in an `endpoint` parameter to the constructor:

```python
culturalSearch = KSamsok(endpoint='https://example.com/')
```

Note that when using a custom endpoint `formatUri()` will still output URLs targeting kulturarvsdata.se and not the custom endpoint. It will accept custom URIs as input.
