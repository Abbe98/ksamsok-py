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
    name = list()
    titles = list()
    descriptions = list()
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
        # meta data patterns
        build_date_pattern = re.compile(r'<ns(?:\d):buildDate>((\d|-)+?)<\/ns(?:\d):buildDate>')
        created_date_pattern = re.compile(r'<ns(?:\d):createdDate>((\d|-)+?)<\/ns(?:\d):createdDate>')
        last_changed_date_pattern = re.compile(r'<ns(?:\d):lastChangedDate>((\d|-)+?)<\/ns(?:\d):lastChangedDate>')
        soch_version_pattern = re.compile(r'<ns(?:\d):ksamsokVersion>((\d|\.)+?)<\/ns(?:\d):ksamsokVersion>')
        service_name_pattern = re.compile(r'<ns(?:\d):serviceName>(.+?)<\/ns(?:\d):serviceName>')
        service_org_pattern = re.compile(r'<ns(?:\d):serviceOrganization>(.+?)<\/ns(?:\d):serviceOrganization>')

        self.meta['build_date'] = self.if_match(build_date_pattern, self.raw_rdf)
        self.meta['created_date'] = self.if_match(created_date_pattern, self.raw_rdf)
        self.meta['last_changed_date'] = self.if_match(last_changed_date_pattern, self.raw_rdf)
        self.meta['soch_version'] = self.if_match(soch_version_pattern, self.raw_rdf)
        self.meta['service'] = self.if_match(service_name_pattern, self.raw_rdf)
        self.meta['service_org'] = self.if_match(service_org_pattern, self.raw_rdf)

        # core patterns
        uri_pattern = re.compile(r'<rdf:Description rdf:about="(.+?)">')
        url_pattern = re.compile(r'<ns(?:\d):url>(.+?)<\/ns(?:\d):url>')
        museumdat_pattern = re.compile(r'<ns(?:\d):museumdatUrl>(.+?)<\/ns(?:\d):museumdatUrl>')
        thumbnail_pattern = re.compile(r'<ns(?:\d):thumbnail>(.+?)<\/ns(?:\d):thumbnail>')
        super_type_pattern = re.compile(r'<ns(?:\d):itemSuperType rdf:resource="(.+?)"\/>')
        type_pattern = re.compile(r'<ns(?:\d):itemSuperType rdf:resource="(.+?)"\/>')
        label_pattern = re.compile(r'<ns(?:\d):itemLabel>(.+?)<\/ns(?:\d):itemLabel>')
        data_quality_pattern = re.compile(r'<ns(?:\d):dataQuality rdf:resource="(.+?)"\/>')

        collection_pattern = re.compile(r'') #LOOP!
        theme_pattern = re.compile(r'') #LOOP!
        subject_pattern = re.compile(r'') #LOOP!
        media_type_pattern = re.compile(r'') #LOOP!
        class_pattern = re.compile(r'') #LOOP!
        name_pattern = re.compile(r'') #LOOP!
        title_pattern = re.compile(r'') #LOOP!
        description_pattern = re.compile(r'') #LOOP!
        key_word_pattern = re.compile(r'') #LOOP!
        motive_key_work_pattern = re.compile(r'') #LOOP!

        self.uri = self.if_match(uri_pattern, self.raw_rdf)
        self.data_quality = self.if_match(data_quality_pattern, self.raw_rdf)
        self.url = self.if_match(uri_pattern, self.raw_rdf)
        self.museumdat = self.if_match(museumdat_pattern, self.raw_rdf)
        self.thumbnail = self.if_match(thumbnail_pattern, self.raw_rdf)
        self.label = self.if_match(label_pattern, self.raw_rdf)
        self.super_type = self.if_match(super_type_pattern, self.raw_rdf)
        self.type = self.if_match(type_pattern, self.raw_rdf)

    def exists(self):
        # should implement utils.validate_request but from local extracted URI
        raise NotImplementedError

    def if_match(self, pattern, target):
        # regex helper
        result = pattern.search(target)
        if result:
            return result.group(1)

        return None
