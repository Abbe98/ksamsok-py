import re
import requests
from lxml import etree

class KSamsok:
    def __init__(self, endpoint = 'https://kulturarvsdata.se/'):
        self.endpoint = endpoint

    def validateRequest(self, url):
        r = requests.head(url)
        return self.validHttpStatus(r.status_code)

    def validHttpStatus(self, status):
        if 200 <= status <= 399:
            return True
        else:
            return False

    def parseRecord(self, record):
        parsed_record = {}

        parsed_record['presentation'] = {}

        r_version = record.xpath('.//pres_version')
        parsed_record['presentation']['version'] = r_version[0].text if 0 < len(r_version) else None

        r_uri = record.xpath('.//pres_entityUri')
        parsed_record['presentation']['uri'] = r_uri[0].text if 0 < len(r_uri) else None

        r_type = record.xpath('.//pres_type')
        parsed_record['presentation']['type'] = r_type[0].text if 0 < len(r_type) else None

        r_organization = record.xpath('.//pres_organization')
        parsed_record['presentation']['organization'] = r_organization[0].text if 0 < len(r_type) else None

        r_id = record.xpath('.//pres_id')
        parsed_record['presentation']['id'] = r_id[0].text if 0 < len(r_id) else None

        r_id_label = record.xpath('.//pres_idLabel')
        parsed_record['presentation']['id_label'] = r_id_label[0].text if 0 < len(r_id_label) else None

        r_item_label = record.xpath('.//pres_itemLabel')
        parsed_record['presentation']['item_label'] = r_item_label[0].text if 0 < len(r_item_label) else None

        parsed_record['presentation']['tags'] = list()
        for tag in record.xpath('.//pres_tag'):
            parsed_record['presentation']['tags'].append(tag.text)

        r_description = record.xpath('.//pres_description')
        parsed_record['presentation']['description'] = r_description[0].text if 0 < len(r_description) else None

        r_content = record.xpath('.//pres_content')
        parsed_record['presentation']['content'] = r_content[0].text if 0 < len(r_content) else None

        r_contexts = record.xpath('.//pres_context')
        parsed_record['presentation']['contexts'] = list()
        for context in r_contexts:
            parsed_context = {}

            c_event = context.xpath('.//pres_event')
            parsed_context['event'] = c_event[0].text if 0 < len(c_event) else None

            c_place_label = context.xpath('.//pres_placeLabel')
            parsed_context['place_label'] = c_place_label[0].text if 0 < len(c_place_label) else None

            c_time_label = context.xpath('.//pres_timeLabel')
            parsed_context['time_label'] = c_time_label[0].text if 0 < len(c_time_label) else None

            c_name_label = context.xpath('.//pres_nameLabel')
            parsed_context['name_label'] = c_name_label[0].text if 0 < len(c_name_label) else None

            if all(value == None for value in parsed_context.values()):
                break

            parsed_record['presentation']['contexts'].append(parsed_context)

        r_coordinates = record.xpath('.//georss_where/gml_Point/gml_coordinates')
        parsed_record['presentation']['coordinates'] = r_coordinates[0].text if 0 < len(r_coordinates) else None

        r_images = record.xpath('.//pres_image')
        parsed_record['presentation']['images'] = list()
        for image in r_images:
            parsed_image = {}

            i_thumbnail = image.xpath('.//pres_src[@type=\'thumbnail\']')
            parsed_image['thumbnail'] = i_thumbnail[0].text if 0 < len(i_thumbnail) else None

            i_lowres = image.xpath('.//pres_src[@type=\'lowres\']')
            parsed_image['lowres'] = i_lowres[0].text if 0 < len(i_lowres) else None

            i_highres = image.xpath('.//pres_src[typec=\'highres\']')
            parsed_image['highres'] = i_highres[0].text if 0 < len(i_highres) else None

            i_by_line = image.xpath('.//pres_byline')
            parsed_image['by_line'] = i_by_line[0].text if 0 < len(i_by_line) else None

            i_motive = image.xpath('.//pres_motive')
            parsed_image['motive'] = i_motive[0].text if 0 < len(i_motive) else None

            i_copyright = image.xpath('.//pres_copyright')
            parsed_image['copyright'] = i_copyright[0].text if 0 < len(i_copyright) else None

            i_license = image.xpath('.//pres_mediaLicense')
            parsed_image['license'] = i_license[0].text if 0 < len(i_license) else None

            i_license_url = image.xpath('.//pres_mediaLicenseUrl')
            parsed_image['license_url'] = i_license_url[0].text if 0 < len(i_license_url) else None

            i_uri = image.xpath('.//pres_mediaUri')
            parsed_image['uri'] = i_uri[0].text if 0 < len(i_uri) else None

            i_url = image.xpath('.//pres_mediaUrl')
            parsed_image['url'] = i_url[0].text if 0 < len(i_url) else None

            parsed_record['presentation']['images'].append(parsed_image)

        parsed_record['presentation']['representations'] = list()
        for representation in record.xpath('.//pres_representations/pres_representation'):
            parsed_record['presentation']['representations'].append(representation.text)

        return parsed_record

    def killXmlNamespaces(self, xml_string):
        xml_string = re.sub('pres:', 'pres_', xml_string)
        xml_string = re.sub('georss:', 'georss_', xml_string)
        xml_string = re.sub('gml:', 'gml_', xml_string)
        xml_string = re.sub('geoF:', 'geoF_', xml_string)
        xml_string = re.sub('rel:', 'rel_', xml_string)
        xml_string = re.sub('xmlns:', 'xmlns_', xml_string)

        return xml_string

    def formatUri(self, uri, uri_format, validate = False):
        default_endpoint = 'http://kulturarvsdata.se/'

        if default_endpoint in uri:
            uri = re.sub(default_endpoint, '', uri)
        elif self.endpoint in uri:
            uri = re.sub(self.endpoint, '', uri)

        uri = re.sub('xml/', '', uri)
        uri = re.sub('rdf/', '', uri)
        uri = re.sub('html/', '', uri)
        uri = re.sub('jsonld/', '', uri)
        uri = re.sub('museumdat/', '', uri)

        # get position of the last /
        try:
            format_index = uri.rindex('/')
        except ValueError:
            return False

        if (validate):
            test_query = self.endpoint + uri[:format_index] + uri[format_index:]
            if not self.validateRequest(test_query):
                return False

        if (uri_format == 'rawurl'):
            return default_endpoint + uri
        elif(uri_format == 'xml'):
            return uri[:format_index] + '/xml' + uri[format_index:]
        elif(uri_format == 'xmlurl'):
            return default_endpoint + uri[:format_index] + '/xml' + uri[format_index:]
        elif(uri_format == 'rdf'):
            return uri[:format_index] + '/rdf' + uri[format_index:]
        elif(uri_format == 'rdfurl'):
            return default_endpoint + uri[:format_index] + '/rdf' + uri[format_index:]
        elif(uri_format == 'html'):
            return uri[:format_index] + '/html' + uri[format_index:]
        elif(uri_format == 'htmlurl'):
            return default_endpoint + uri[:format_index] + '/html' + uri[format_index:]
        elif(uri_format == 'jsonld'):
            return uri[:format_index] + '/jsonld' + uri[format_index:]
        elif(uri_format == 'jsonldurl'):
            return default_endpoint + uri[:format_index] + '/jsonld' + uri[format_index:]
        elif(uri_format == 'museumdat'):
            return uri[:format_index] + '/museumdat' + uri[format_index:]
        elif(uri_format == 'museumdaturl'):
            return default_endpoint + uri[:format_index] + '/museumdat' + uri[format_index:]
        else:
            return uri

    def kringlaToUri(self, kringla, uri_format, validate = False):
        if 'http://www.kringla.nu/kringla/objekt?' not in kringla:
            return False

        re_matches = re.search(r'(\?|&)referens=(.+)($|&)', kringla)

        if not re_matches.group(2):
            return False
        
        return self.formatUri(re_matches.group(2), uri_format, validate)

    def getObject(self, uri):
        request_query = self.formatUri(uri, 'xmlurl')

        if not request_query:
            return False

        r = requests.get(request_query)
        if not self.validHttpStatus(r.status_code):
            return False

        # remove all XML namespaces, and push the bytes to etree.XML
        xml = etree.XML(str.encode(self.killXmlNamespaces(r.text)))

        return self.parseRecord(xml)

    def cql(self, query, start, hits = 60):
        # create the request URL
        request_query = self.endpoint + 'ksamsok/api?method=search&hitsPerPage=' + str(hits) + '&startRecord=' + str(start) + '&query=' + query + '&recordSchema=presentation'

        r = requests.get(request_query)
        if not self.validHttpStatus(r.status_code):
            return False

        # remove all XML namespaces, and push the bytes to etree.XML
        xml = etree.XML(str.encode(self.killXmlNamespaces(r.text)))

        result = {}
        hits = xml.xpath('/result/totalHits')
        result['hits'] = hits[0].text if 0 < len(hits) else None

        result['records'] = list()
        records = xml.xpath('/result/records/record/pres_item')
        for record in records:
            result['records'].append((self.parseRecord(record)))

        return result

    def cqlGenerator(self, query):
        start = 0
        has_more = True

        while has_more:
            results = self.cql(query, start, 500)['records']
            for item in results:
                yield item

            if len(results) < 500:
                has_more = False

            start += 500

    def search(self, text, start, hits, images = False):
        cql = 'text=' + text
        # in erlier versions we added &thumbnailExists=j to url
        if images:
            cql = cql + ' AND thumbnailExists=j'

        return self.cql(cql, start, hits)

    def geoSearch(self, west, south, east, north, start, hits = 60):
        cql = 'boundingBox=/WGS84%20"' + str(west) + ' ' + str(south) + ' ' + str(east) + ' ' + str(north)

        return self.cql(cql, start, hits)

    def getRelations(self, uri, infer_same_as = False):
        uri = self.formatUri(uri, 'raw')

        if not uri:
            return False

        request_query = self.endpoint + 'ksamsok/api?&method=getRelations&relation=all&objectId=' + uri

        if infer_same_as:
            request_query += '&inferSameAs=yes'

        r = requests.get(request_query)
        if not self.validHttpStatus(r.status_code):
            return False

        xml = etree.XML(r.content)

        result = list()
        relations = xml.xpath('/result/relations/relation')
        for relation in relations:
            parsed_relation = {}

            parsed_relation['uri'] = relation.text
            parsed_relation['source'] = relation.get('source')
            parsed_relation['type'] = relation.get('type')

            result.append(parsed_relation)

        return result

    def getHints(self, string, count = 5):
        request_query = self.endpoint + 'ksamsok/api?method=searchHelp&index=text&prefix=' + string + '*&maxValueCount=' + str(count)

        r = requests.get(request_query)
        if not self.validHttpStatus(r.status_code):
            return False

        xml = etree.XML(r.content)

        result = list()
        terms = xml.xpath('/result/terms/term')
        for term in terms:
            parsed_term = {}

            parsed_term['count'] = term.xpath('.//count')[0].text
            parsed_term['value'] = term.xpath('.//value')[0].text

            result.append(parsed_term)

        return result
