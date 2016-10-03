import requests, re, sys
from lxml import etree

class KSamsok:
    def __init__(self, key, endpoint = 'http://kulturarvsdata.se/'):
        self.key = key
        self.endpoint = endpoint

        test_query = self.endpoint + 'ksamsok/api?x-api=' + key + '&method=search&query=text%3D"test"&recordSchema=presentation'

        if not self.validateRequest(test_query):
            raise Exception('Bad API key or inaccessible endpoint.')

    def validateRequest(self, url):
        r = requests.get(url)

        if 200 <= r.status_code <= 399:
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

            c_event = context.xpath('.//event')
            parsed_context['event'] = c_event[0].text if 0 < len(c_event) else None
            
            c_place_label = context.xpath('.//place_label')
            parsed_context['place_label'] = c_place_label[0].text if 0 < len(c_place_label) else None
            
            c_time_label = context.xpath('.//time_label')
            parsed_context['time_label'] = c_time_label[0].text if 0 < len(c_time_label) else None
            
            c_name_label = context.xpath('.//name_label')
            parsed_context['name_label'] = c_name_label[0].text if 0 < len(c_name_label) else None
            
            parsed_record['presentation']['contexts'].append(parsed_context)

        # what about areas? not supported in KSamsök-PHP?
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

        parsed_record['presentation']['references'] = list()
        for reference in record.xpath('.//pres_references/pres_reference'):
            parsed_record['presentation']['references'].append(reference.text)

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
        if self.endpoint in uri:
            uri = re.sub(self.endpoint, '', uri)

        uri = re.sub('xml/', '', uri)
        uri = re.sub('rdf/', '', uri)
        uri = re.sub('html/', '', uri)

        # get position of the last /
        format_index = uri.rindex('/')

        if (validate):
            test_query = self.endpoint + uri[:format_index] + '/xml' + uri[format_index:]
            if not self.validateRequest(test_query):
                return False

        if (uri_format == 'rawurl'):
            return self.endpoint + uri
        elif(uri_format == 'xml'):
            return uri[:format_index] + '/xml' + uri[format_index:]
        elif(uri_format == 'xmlurl'):
            return self.endpoint + uri[:format_index] + '/xml' + uri[format_index:]
        elif(uri_format == 'rdf'):
            return uri[:format_index] + '/rdf' + uri[format_index:]
        elif(uri_format == 'rdfurl'):
            return self.endpoint + uri[:format_index] + '/rdf' + uri[format_index:]
        elif(uri_format == 'html'):
            return uri[:format_index] + '/html' + uri[format_index:]
        elif(uri_format == 'htmlurl'):
            return self.endpoint + uri[:format_index] + '/html' + uri[format_index:]
        else:
            return uri

    def getObject(self, uri):
        request_query = self.formatUri(uri, 'xmlurl')

        r = requests.get(request_query)
        # remove all XML namespaces, and push the bytes to etree.XML
        xml = etree.XML(str.encode(self.killXmlNamespaces(r.text)))

        return self.parseRecord(xml)

    def search(self, text, start, hits, images = False):
        #create the request URL
        request_query = self.endpoint + 'ksamsok/api?x-api=' + self.key + '&method=search&hitsPerPage=' + str(hits) + '&startRecord=' + str(start) + '&query=text%3D"' + text + '"&recordSchema=presentation'

        # if images = true add &thumbnailExists=j to url
        if images: 
            request_query = request_query + '&thumbnailExists=j'

        r = requests.get(request_query)
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