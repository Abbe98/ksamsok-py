import re
import requests

def kringla_to_uri(kringla):
    if 'http://www.kringla.nu/kringla/objekt?' not in kringla:
        return False

    re_matches = re.search(r'(\?|&)referens=(.+)($|&)', kringla)

    if not re_matches.group(2):
        return False

    return kulturarvsdata_to_uri(re_matches.group(2))

def kulturarvsdata_to_uri(kulturarvsdata):
    root = 'http://kulturarvsdata.se/'

    uri = kulturarvsdata
    if root not in kulturarvsdata:
        uri = root + uri

    uri = re.sub('xml/', '', uri)
    uri = re.sub('rdf/', '', uri)
    uri = re.sub('html/', '', uri)
    uri = re.sub('jsonld/', '', uri)
    uri = re.sub('museumdat/', '', uri)

    if uri.endswith('/'):
        uri = uri[:-1]

    if uri.count('/') is not 5:
        return False

    return uri

def kulturarvsdata_to_id(kulturarvsdata):
    root = 'http://kulturarvsdata.se/'

    r_id = kulturarvsdata
    if root in kulturarvsdata:
        r_id = re.sub(root, '', r_id)

    r_id = re.sub('xml/', '', r_id)
    r_id = re.sub('rdf/', '', r_id)
    r_id = re.sub('html/', '', r_id)
    r_id = re.sub('jsonld/', '', r_id)
    r_id = re.sub('museumdat/', '', r_id)

    if r_id.endswith('/'):
        r_id = r_id[:-1]

    if r_id.count('/') is not 2:
        return False

    return r_id

def province_uri_to_string(uri):
    if uri.endswith('Bl'): return 'Blekinge'
    if uri.endswith('Bo'): return 'Bohuslän'
    if uri.endswith('Dl'): return 'Dalarna'
    if uri.endswith('Ds'): return 'Dalsland'
    if uri.endswith('Go'): return 'Gotland'
    if uri.endswith('Gä'): return 'Gästrikland'
    if uri.endswith('Ha'): return 'Halland'
    if uri.endswith('Hs'): return 'Hälsingland'
    if uri.endswith('Hr'): return 'Härjedalen'
    if uri.endswith('Jä'): return 'Jämtland'
    if uri.endswith('La'): return 'Lappland'
    if uri.endswith('Me'): return 'Medelpad'
    if uri.endswith('Nb'): return 'Norrbotten'
    if uri.endswith('Nä'): return 'Närke'
    if uri.endswith('Sk'): return 'Skåne'
    if uri.endswith('Sm'): return 'Småland'
    if uri.endswith('Sö'): return 'Södermanland'
    if uri.endswith('Up'): return 'Uppland'
    if uri.endswith('Vr'): return 'Värmland'
    if uri.endswith('Vb'): return 'Västerbotten'
    if uri.endswith('Vg'): return 'Västergötland'
    if uri.endswith('Vs'): return 'Västmanland'
    if uri.endswith('Ån'): return 'Ångermanland'
    if uri.endswith('Öl'): return 'Öland'
    if uri.endswith('Ög'): return 'Östergötland'

    return False

def validate_uri(uri):
    return validate_request(uri)

def validate_request(url):
    try:
        r = requests.head(url)
        return valid_http_status(r.status_code)
    except:
        return False

def valid_http_status(status):
    if 200 <= status <= 399:
        return True
    else:
        return False
