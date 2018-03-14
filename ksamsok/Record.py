import re

import requests

from .utils import validate_request
from .utils import valid_http_status

class Record:
    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as file:
            return cls(file.read())

    @classmethod
    def from_string(cls, record):
        return cls(record)

    @classmethod
    def from_uri(cls, uri):
        r = requests.get(uri)
        if not valid_http_status(r.status_code):
            #TODO better exception
            raise Exception('URI responded with http status code: ' + str(r.status_code))

        return cls(r.text)

    def __init__(self, record):
        self.raw_rdf = None

        self.meta = {}

        self.uri = None
        self.url = None
        self.museumdat = None
        self.thumbnail = None
        self.super_type = None
        self.type = None
        self.label = None

        self.collections = list()
        self.themes = list()
        self.subjects = list()
        self.media_types = list()
        self.classes = list()
        self.class_names = list()
        self.titles = list()
        self.key_words = list()
        self.motive_key_words = list()

        self.colors = list()
        self.techniques = list()
        self.styles = list()

        self.names = list()
        self.specifications = list()
        self.descriptions = list()
        self.materials = list()
        self.numbers = list()
        self.measurements = list()

        self.images = list()

        self.raw_rdf = record
        self.parse()

    def parse(self):
        # get namespace keys
        ksamsok_ns = self.get_namespace('http://kulturarvsdata.se/ksamsok#')

        uri_pattern = re.compile('<(?:rdf:Description|Entity) rdf:about="(.+?)">')
        self.uri = self.if_match(uri_pattern, self.raw_rdf)
        if not self.uri:
            #TODO better exception
            raise Exception('Could not parse URI from given record.')

        # meta data patterns
        build_date_pattern = re.compile(r'<{0}buildDate>((\d|-)+?)<\/{0}buildDate>'.format(ksamsok_ns))
        created_date_pattern = re.compile(r'<{0}createdDate>((\d|-)+?)<\/{0}createdDate>'.format(ksamsok_ns))
        last_changed_date_pattern = re.compile(r'<{0}lastChangedDate>((\d|-)+?)<\/{0}lastChangedDate>'.format(ksamsok_ns))
        soch_version_pattern = re.compile(r'<{0}ksamsokVersion>((\d|\.)+?)<\/{0}ksamsokVersion>'.format(ksamsok_ns))
        service_name_pattern = re.compile(r'<{0}serviceName>(.+?)<\/{0}serviceName>'.format(ksamsok_ns))
        service_org_pattern = re.compile(r'<{0}serviceOrganization>(.+?)<\/{0}serviceOrganization>'.format(ksamsok_ns))

        self.meta['build_date'] = self.if_match(build_date_pattern, self.raw_rdf)
        self.meta['created_date'] = self.if_match(created_date_pattern, self.raw_rdf)
        self.meta['last_changed_date'] = self.if_match(last_changed_date_pattern, self.raw_rdf)
        self.meta['soch_version'] = self.if_match(soch_version_pattern, self.raw_rdf)
        self.meta['service'] = self.if_match(service_name_pattern, self.raw_rdf)
        self.meta['service_org'] = self.if_match(service_org_pattern, self.raw_rdf)

        # core patterns
        url_pattern = re.compile(r'<{0}url>(.+?)<\/{0}url>'.format(ksamsok_ns))
        museumdat_pattern = re.compile(r'<{0}museumdatUrl>(.+?)<\/{0}museumdatUrl>'.format(ksamsok_ns))
        thumbnail_pattern = re.compile(r'<{0}thumbnail>(.+?)<\/{0}thumbnail>'.format(ksamsok_ns))
        super_type_pattern = re.compile(r'<{0}itemSuperType rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        type_pattern = re.compile(r'<{0}itemType rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        label_pattern = re.compile(r'<{0}itemLabel>(.+?)<\/{0}itemLabel>'.format(ksamsok_ns))
        data_quality_pattern = re.compile(r'<{0}dataQuality rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))

        self.data_quality = self.if_match(data_quality_pattern, self.raw_rdf)
        self.url = self.if_match(url_pattern, self.raw_rdf)
        self.museumdat = self.if_match(museumdat_pattern, self.raw_rdf)
        self.thumbnail = self.if_match(thumbnail_pattern, self.raw_rdf)
        self.label = self.if_match(label_pattern, self.raw_rdf)
        self.super_type = self.if_match(super_type_pattern, self.raw_rdf)
        self.type = self.if_match(type_pattern, self.raw_rdf)

        # iterative value patterns
        collection_pattern = re.compile(r'<{0}collection>(.+?)<\/{0}collection>'.format(ksamsok_ns))
        theme_pattern = re.compile(r'<{0}theme rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        subject_pattern = re.compile(r'<{0}subject rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        media_type_pattern = re.compile(r'<{0}mediaType rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        class_pattern = re.compile(r'<{0}itemClass rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        class_name_pattern = re.compile(r'<{0}itemClassName>(.+?)<\/{0}itemClassName>'.format(ksamsok_ns))
        title_pattern = re.compile(r'<{0}itemTitle>(.+?)<\/{0}itemTitle>'.format(ksamsok_ns))
        key_word_pattern = re.compile(r'<{0}itemKeyWord>(.+?)<\/{0}itemKeyWord>'.format(ksamsok_ns))
        motive_key_word_pattern = re.compile(r'<{0}itemMotiveWord>(.+?)<\/{0}itemMotiveWord>'.format(ksamsok_ns))

        color_pattern = re.compile(r'<{0}itemColor>(.+?)<\/{0}itemColor>'.format(ksamsok_ns))
        technique_pattern = re.compile(r'<{0}itemTechnique>(.+?)<\/{0}itemTechnique>'.format(ksamsok_ns))
        style_pattern = re.compile(r'<{0}itemStyle>(.+?)<\/{0}itemStyle>'.format(ksamsok_ns))

        for c in re.finditer(collection_pattern, self.raw_rdf):
            self.collections.append(c.group(1))

        for t in re.finditer(theme_pattern, self.raw_rdf):
            self.themes.append(t.group(1))

        for s in re.finditer(subject_pattern, self.raw_rdf):
            self.subjects.append(s.group(1))

        for mt in re.finditer(media_type_pattern, self.raw_rdf):
            self.media_types.append(mt.group(1).split('#')[1])

        for c in re.finditer(class_pattern, self.raw_rdf):
            self.classes.append(c.group(1))

        for cn in re.finditer(class_name_pattern, self.raw_rdf):
            self.class_names.append(cn.group(1))

        for t in re.finditer(title_pattern, self.raw_rdf):
            self.titles.append(t.group(1))

        for kw in re.finditer(key_word_pattern, self.raw_rdf):
            self.key_words.append(kw.group(1))

        for mkw in re.finditer(motive_key_word_pattern, self.raw_rdf):
            self.motive_key_words.append(mkw.group(1))

        for c in re.finditer(color_pattern, self.raw_rdf):
            self.colors.append(c.group(1))

        for t in re.finditer(technique_pattern, self.raw_rdf):
            self.techniques.append(t.group(1))

        for s in re.finditer(style_pattern, self.raw_rdf):
            self.styles.append(s.group(1))

        type_pattern = re.compile(r'<{0}type>(.+?)<\/{0}type>'.format(ksamsok_ns))

        measurement_nodes = self.get_nodes('itemMeasurement', 'ItemMeasurement', ksamsok_ns)
        value_pattern = re.compile(r'<{0}value>(.+?)<\/{0}value>'.format(ksamsok_ns))
        unit_pattern = re.compile(r'<{0}unit>(.+?)<\/{0}unit>'.format(ksamsok_ns))
        qualifier_pattern = re.compile(r'<{0}qualifier>(.+?)<\/{0}qualifier>'.format(ksamsok_ns))

        for node in measurement_nodes:
            measurement = {}
            measurement['type'] = self.if_match(type_pattern, node)
            measurement['value'] = self.if_match(value_pattern, node)
            measurement['unit'] = self.if_match(unit_pattern, node)
            measurement['qualifier'] = self.if_match(qualifier_pattern, node)

            self.measurements.append(measurement)

        name_nodes = self.get_nodes('itemName', 'ItemName', ksamsok_ns)
        name_pattern = re.compile(r'<{0}name>(.+?)<\/{0}name>'.format(ksamsok_ns))
        for node in name_nodes:
            name = {}
            name['type'] = self.if_match(type_pattern, node)
            name['name'] = self.if_match(name_pattern, node)

            self.names.append(name)

        number_nodes = self.get_nodes('itemNumber', 'ItemNumber', ksamsok_ns)
        number_pattern = re.compile(r'<{0}number>(.+?)<\/{0}number>'.format(ksamsok_ns))
        for node in number_nodes:
            number = {}
            number['type'] = self.if_match(type_pattern, node)
            number['number'] = self.if_match(number_pattern, node)

            self.numbers.append(number)

        spec_nodes = self.get_nodes('itemSpecification', 'ItemSpecification', ksamsok_ns)
        spec_pattern = re.compile(r'<{0}spec>(.+?)<\/{0}spec>'.format(ksamsok_ns))
        for node in spec_nodes:
            spec = {}
            spec['type'] = self.if_match(type_pattern, node)
            spec['spec'] = self.if_match(spec_pattern, node)

            self.specifications.append(spec)

        material_nodes = self.get_nodes('itemMaterial', 'ItemMaterial', ksamsok_ns)
        material_pattern = re.compile(r'<{0}material>(.+?)<\/{0}material>'.format(ksamsok_ns))
        for node in material_nodes:
            material = {}
            material['type'] = self.if_match(type_pattern, node)
            material['material'] = self.if_match(material_pattern, node)

            self.materials.append(material)

        desc_nodes = self.get_nodes('itemDescription', 'ItemDescription', ksamsok_ns)
        desc_pattern = re.compile(r'<{0}desc>(.+?)<\/{0}desc>'.format(ksamsok_ns))
        for node in desc_nodes:
            desc = {}
            desc['type'] = self.if_match(type_pattern, node)
            desc['desc'] = self.if_match(desc_pattern, node)

            self.descriptions.append(desc)

        image_nodes = self.get_nodes('image', 'Image', ksamsok_ns)
        # media_type_pattern
        thumbnail_pattern_media = re.compile(r'<{0}thumbnailSource>(.+?)<\/{0}thumbnailSource>'.format(ksamsok_ns))
        lowres_pattern = re.compile(r'<{0}lowresSource>(.+?)<\/{0}lowresSource>'.format(ksamsok_ns))
        highres_pattern = re.compile(r'<{0}highresSource>(.+?)<\/{0}highresSource>'.format(ksamsok_ns))
        byline_pattern = re.compile(r'<{0}byline>(.+?)<\/{0}byline>'.format(ksamsok_ns))
        copyright_pattern = re.compile(r'<{0}copyright>(.+?)<\/{0}copyright>'.format(ksamsok_ns))
        motive_key_word_pattern_media = re.compile(r'<{0}mediaMotiveWord>(.+?)<\/{0}mediaMotiveWord>'.format(ksamsok_ns))
        license_pattern = re.compile(r'<{0}mediaLicense rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))
        license_url_pattern = re.compile(r'<{0}mediaLicenseUrl rdf:resource="(.+?)"(?:|\s)\/>'.format(ksamsok_ns))

        for node in image_nodes:
            image = {}
            image['thumbnail'] = self.if_match(thumbnail_pattern_media, node)
            image['lowres'] = self.if_match(lowres_pattern, node)
            image['highres'] = self.if_match(highres_pattern, node)
            image['byline'] = self.if_match(byline_pattern, node)
            image['copyright'] = self.if_match(copyright_pattern, node)
            image['license'] = self.if_match(license_pattern, node)
            image['license_url'] = self.if_match(license_url_pattern, node)

            image['media_type'] = self.if_match(media_type_pattern, node)
            image['media_type'] = image['media_type'].split('#')[1] if image['media_type'] else None

            image['motive_key_words'] = list()
            for mkw in re.finditer(motive_key_word_pattern_media, node):
                image['motive_key_words'].append(mkw.group(1))

            self.images.append(image)

    def exists(self):
        # should implement utils.validate_request but from local extracted URI
        raise NotImplementedError

    def if_match(self, pattern, target):
        # regex helper
        result = pattern.search(target)
        if result:
            return result.group(1)

        return None

    def get_nodes(self, pointer, tag, ksamsok_ns):
        result = list()

        node_pointer_pattern = re.compile(r'<{1}{0} rdf:nodeID="(.+)"(?:|\s)\/>'.format(pointer, ksamsok_ns))
        for node_id in re.finditer(node_pointer_pattern, self.raw_rdf):
            node_pattern = re.compile(r'<(?:{1}{0}|rdf:Description) rdf:nodeID="{2}">((?:.|\n)+?)<\/(?:{1}{0}|rdf:Description)>'.format(tag, ksamsok_ns, node_id.group(1)))
            for node in re.finditer(node_pattern, self.raw_rdf):
                result.append(node.group(1))

        return result

    def get_namespace(self, target):
        ns_pattern = re.compile(r'xmlns(?:|:((?:\w|\d)+))?="{0}"'.format(target))
        ns = self.if_match(ns_pattern, self.raw_rdf)
        if ns:
            return ns + ':'
        else:
            return ''

    def __repr__(self):
        return '{0} {1}'.format(self.__class__, self.uri)
