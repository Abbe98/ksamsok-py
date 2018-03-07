import re

import requests

from .utils import validate_request
from .utils import valid_http_status

class Record:
    raw_rdf = None

    meta = {}

    uri = None
    url = None
    museumdat = None
    thumbnail = None
    super_type = None
    type = None
    label = None

    collections = list()
    themes = list()
    subjects = list()
    media_types = list()
    classes = list()
    class_names = list()
    titles = list()
    key_words = list()
    motive_key_words = list()

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
        super_type_pattern = re.compile(r'<{0}itemSuperType rdf:resource="(.+?)"(?:\s)\/>'.format(ksamsok_ns))
        type_pattern = re.compile(r'<{0}itemType rdf:resource="(.+?)"(?:\s)\/>'.format(ksamsok_ns))
        label_pattern = re.compile(r'<{0}itemLabel>(.+?)<\/{0}itemLabel>'.format(ksamsok_ns))
        data_quality_pattern = re.compile(r'<{0}dataQuality rdf:resource="(.+?)"(?:\s)\/>'.format(ksamsok_ns))

        self.data_quality = self.if_match(data_quality_pattern, self.raw_rdf)
        self.url = self.if_match(url_pattern, self.raw_rdf)
        self.museumdat = self.if_match(museumdat_pattern, self.raw_rdf)
        self.thumbnail = self.if_match(thumbnail_pattern, self.raw_rdf)
        self.label = self.if_match(label_pattern, self.raw_rdf)
        self.super_type = self.if_match(super_type_pattern, self.raw_rdf)
        self.type = self.if_match(type_pattern, self.raw_rdf)

        collection_pattern = re.compile(r'') #LOOP!
        theme_pattern = re.compile(r'') #LOOP!
        subject_pattern = re.compile(r'') #LOOP!
        media_type_pattern = re.compile(r'') #LOOP!
        class_pattern = re.compile(r'') #LOOP!
        class_name_pattern = re.compile(r'') #LOOP!
        title_pattern = re.compile(r'') #LOOP!
        description_pattern = re.compile(r'') #LOOP!
        key_word_pattern = re.compile(r'') #LOOP!
        motive_key_work_pattern = re.compile(r'') #LOOP!

    def exists(self):
        # should implement utils.validate_request but from local extracted URI
        raise NotImplementedError

    def if_match(self, pattern, target):
        # regex helper
        result = pattern.search(target)
        if result:
            return result.group(1)

        return None

    def get_namespace(self, target):
        ns_pattern = re.compile(r'xmlns(?:|:(.+))?="{0}"'.format(target))
        ns = self.if_match(ns_pattern, self.raw_rdf)
        if ns:
            return ns + ':'
        else:
            return ''
