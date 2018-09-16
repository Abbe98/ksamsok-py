import pytest

from ksamsok import Record

def test_from_string():
    # we are only testing that the string results in a Record instance with 'raw_rdf' attribute
    # the fact that it's invalid should be tested by the parser.
    test_string = '<?xml version="1.0" encoding="UTF-8"?><rdf:RDF>dummy</rdf:RDF>'

    with pytest.raises(Exception) as excinfo:
        record = Record.from_string(test_string)
        assert record.raw_rdf == test_string

        assert 'Could not parse URI from given record.' in str(excinfo.value)

def test_from_file():
    record = Record.from_file('tests/resources/KBGF051559.rdf')

    assert record.raw_rdf.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert record.raw_rdf.endswith('</rdf:RDF>')

@pytest.mark.online
def test_from_uri():
    record = Record.from_uri('http://kulturarvsdata.se/raa/bbrm/21200000000487')

    assert record.raw_rdf.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert record.raw_rdf.endswith('</rdf:RDF>')

def test_not_able_to_parse_error():
    with pytest.raises(Exception) as excinfo:
        Record.from_string('crap')
        assert 'Could not parse URI from given record.' in str(excinfo.value)

def test_parse_meta_data():
    record = Record.from_file('tests/resources/record_with_meta_only.rdf')

    assert record.meta['build_date'] == '2018-02-27'
    assert record.meta['created_date'] == '2018-02-27'
    assert record.meta['last_changed_date'] == '2017-06-28'
    assert record.meta['service'] == 'object'
    assert record.meta['service_org'] == 'MILI'
    assert record.meta['soch_version'] == '1.1'

def test_parse_core_values():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert record.uri == 'http://kulturarvsdata.se/inst/service/objekt-id'
    assert record.url == 'https://example.com/url'
    assert record.museumdat == 'https://example.com/museumdat'
    assert record.thumbnail == 'https://example.com/thumbnail.jpg'
    assert record.super_type == 'http://kulturarvsdata.se/resurser/EntitySuperType#specTyp'
    assert record.label == 'item label'
    assert record.type == 'http://kulturarvsdata.se/resurser/EntityType#specTyp'

def test_parse_iterative_values():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert isinstance(record.collections, list)
    assert isinstance(record.themes, list)
    assert isinstance(record.subjects, list)
    assert isinstance(record.media_types, list)
    assert isinstance(record.classes, list)
    assert isinstance(record.class_names, list)
    assert isinstance(record.titles, list)
    assert isinstance(record.key_words, list)
    assert isinstance(record.motive_key_words, list)
    assert isinstance(record.colors, list)
    assert isinstance(record.techniques, list)
    assert isinstance(record.styles, list)

    assert record.collections[0] == 'Samlingsnamn1'
    assert record.collections[1] == 'Samlingsnamn2'

    assert record.themes[0] == 'http://kulturarvsdata.se/resurser/Theme#tema1'
    assert record.themes[1] == 'http://example.com/resurser/Theme#tema2'

    assert record.subjects[0] == 'http://kulturarvsdata.se/resurser/Subject#specAmne1'
    assert record.subjects[1] == 'http://kulturarvsdata.se/resurser/Subject#specAmne2'
    assert record.subjects[2] == 'http://kulturarvsdata.se/resurser/Subject#specAmne3'

    assert record.media_types[0] == 'specMediatyp1'
    assert record.media_types[1] == 'specMediatyp2'

    assert record.classes[0] == 'http://kulturarvsdata.se/resurser/EntityClass/outline#class1'
    assert record.classes[1] == 'http://kulturarvsdata.se/resurser/EntityClass/outline#class2'

    assert record.class_names[0] == 'Klass eller kategori 1'
    assert record.class_names[1] == 'Klass eller kategori 2'

    assert record.titles[0] == 'Titel eller verksnamn 1'
    assert record.titles[1] == 'Titel eller verksnamn 2'

    assert record.key_words[0] == 'Nyckelord 1'
    assert record.key_words[1] == 'Nyckelord 2'

    assert record.motive_key_words[0] == 'Motivord 1'
    assert record.motive_key_words[1] == 'Motivord 2'

    assert record.colors[0] == 'blå'
    assert record.colors[1] == 'vit'

    assert record.techniques[0] == 'slipad'
    assert record.techniques[1] == 'filad'

    assert record.styles[0] == 'gustaviansk'
    assert record.styles[1] == 'abbeiansk'

def test_parse_empty_iterative_values():
    record = Record.from_file('tests/resources/record_with_meta_only.rdf')

    assert isinstance(record.collections, list)
    assert isinstance(record.themes, list)
    assert isinstance(record.subjects, list)
    assert isinstance(record.media_types, list)
    assert isinstance(record.classes, list)
    assert isinstance(record.class_names, list)
    assert isinstance(record.titles, list)
    assert isinstance(record.key_words, list)
    assert isinstance(record.motive_key_words, list)
    assert isinstance(record.colors, list)
    assert isinstance(record.techniques, list)
    assert isinstance(record.styles, list)

    assert len(record.collections) == 0
    assert len(record.themes) == 0
    assert len(record.subjects) == 0
    assert len(record.media_types) == 0
    assert len(record.class_names) == 0
    assert len(record.titles) == 0
    assert len(record.key_words) == 0
    assert len(record.motive_key_words) == 0
    assert len(record.colors) == 0
    assert len(record.techniques) == 0
    assert len(record.styles) == 0

def test_all_empty_except_uri():
    # although not a valid SOCH 1.1 RDF we should be fogiving and support it
    test_string = '''<?xml version="1.0" encoding="UTF-8"?>
                    <rdf:RDF 
                        xmlns:ns1="http://kulturarvsdata.se/ksamsok#" 
                        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                        <rdf:Description rdf:about="http://kulturarvsdata.se/KBG/photo/KBGF051559">
                        </rdf:Description>
                    </rdf:RDF>
                 '''

    record = Record.from_string(test_string)

    assert record.uri == 'http://kulturarvsdata.se/KBG/photo/KBGF051559'


def test_parse_named_nodes():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert isinstance(record.names, list)
    assert isinstance(record.specifications, list)
    assert isinstance(record.descriptions, list)
    assert isinstance(record.materials, list)
    assert isinstance(record.numbers, list)
    assert isinstance(record.measurements, list)

    assert record.measurements[0]['type'] == 'Typ av mått, t ex "längd"'
    assert record.measurements[0]['unit'] == 'Enhet, t ex "mm"'
    assert record.measurements[0]['value'] == 'Värde, t ex "23"'
    assert record.measurements[0]['qualifier'] == 'Specifikation av vad som mäts, t ex "egg", "före konservering"'

    assert record.names[0]['type'] == 'Typ av namn, t ex "sakord"'
    assert record.names[0]['name'] == 'Etikett som beskriver objektet'

    assert record.names[1]['type'] == 'kul namn'
    assert record.names[1]['name'] == 'abbe'

    assert record.numbers[0]['type'] == 'Typ av numering, t ex "inventarienummer"'
    assert record.numbers[0]['number'] == 'Nummer'

    assert record.specifications[0]['type'] == 'Typ av specifikation, t ex "produkttyp" eller "modell"'
    assert record.specifications[0]['spec'] == 'Modellbeteckning eller liknande'

    assert record.materials[0]['type'] == 'Typ av material, t ex "huvudmaterial" eller "tilläggsmaterial"'
    assert record.materials[0]['material'] == 'Material, t ex "sten"'

    assert record.descriptions[0]['type'] == 'Typ av beskrivning, t ex "föremålsbeskrivning"'
    assert record.descriptions[0]['desc'] == 'Beskrivning, även ostrukturerad text för fritextsökning'

def test_parse_blank_nodes():
    record = Record.from_file('tests/resources/raa_fmi_10024000190001.rdf')

    assert record.names[0]['type'] == 'Lämningstyp'
    assert record.names[0]['name'] == 'Fångstgård'
    
    assert record.specifications[0]['type'] == 'Anmärkning'
    assert record.specifications[0]['spec'] == 'Detta kan vara en fornlämning.'

    assert record.descriptions[0]['type'] == 'Beskrivning'
    assert record.descriptions[0]['desc'] == 'Varggård'
    assert record.descriptions[1]['type'] == 'Orientering'
    assert record.descriptions[1]['desc'] == 'Ca 10 m Ö om vägen Giboda-Vavd.'

def test_parse_images():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert record.images[0]['media_type'] == 'specMediatyp'
    assert record.images[0]['thumbnail'] == 'Länk till källa för bilden 0'
    assert record.images[0]['lowres'] == 'Länk till källa för bilden 1'
    assert record.images[0]['highres'] == 'Länk till källa för bilden 2'
    assert record.images[0]['byline'] == 'Bildttext som ska innehålla fotograf och organisation'
    assert record.images[0]['copyright'] == 'Organisation/Person som äger bilden'
    assert record.images[0]['license'] == 'http://kulturarvsdata.se/resurser/License#specLicens'
    assert record.images[0]['license_url'] == 'http://creativecommons.org/licenses/by/2.5/se/'
    assert len(record.images[0]['motive_key_words']) == 2
    assert record.images[0]['motive_key_words'][0] == 'Motivord'
    assert record.images[0]['motive_key_words'][1] == 'Fler motivord'

    assert record.images[1]['media_type'] == 'specMediatyp2'
    assert record.images[1]['thumbnail'] == 'Länk till källa för bilden 2'
    assert record.images[1]['lowres'] == 'Länk till källa för bilden 2'
    assert record.images[1]['highres'] == 'Länk till källa för bilden 2'
    assert record.images[1]['byline'] == 'Bildttext som ska innehålla fotograf och organisation 2'
    assert record.images[1]['copyright'] == 'Organisation/Person som äger bilden 2'
    assert record.images[1]['license'] == 'http://kulturarvsdata.se/resurser/License#specLicens1'
    assert record.images[1]['license_url'] == 'http://creativecommons.org/licenses/by/2.5/no/'
    assert len(record.images[1]['motive_key_words']) == 2
    assert record.images[1]['motive_key_words'][0] == 'Motivord 1'
    assert record.images[1]['motive_key_words'][1] == 'Fler motivord'

def test_parse_media():
    record = Record.from_file('tests/resources/full_record.rdf')

    assert record.media[0]['media_type'] == 'specMediatyp1'
    assert record.media[0]['byline'] == 'Text som ska innehålla skapare och organisation 1'
    assert record.media[0]['copyright'] == 'Organisation/Person som äger filen 1'
    assert record.media[0]['link'] == 'https://example.com/example.mp4'
    assert record.media[0]['license'] == 'http://kulturarvsdata.se/resurser/License#specLicens1'
    assert record.media[0]['license_url'] == 'http://creativecommons.org/licenses/by/2.5/no/'

    assert record.media[1]['media_type'] == 'specMediatyp2'
    assert record.media[1]['byline'] == 'Text som ska innehålla skapare och organisation 2'
    assert record.media[1]['copyright'] == 'Organisation/Person som äger filen 2'
    assert record.media[1]['link'] == 'https://example.com/example.mp3'
    assert record.media[1]['license'] == 'http://kulturarvsdata.se/resurser/License#specLicens2'
    assert record.media[1]['license_url'] == 'http://creativecommons.org/licenses/by/2.5/nn/'
