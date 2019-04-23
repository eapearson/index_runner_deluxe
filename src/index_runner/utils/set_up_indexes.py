import requests
import json
from .config import get_config

config = get_config()

es_host = config['elasticsearch_host']
es_port = config['elasticsearch_port']

es_data_type = config["elasticsearch_data_type"]
es_url = "http://" + es_host + ":" + str(es_port)

es_index_prefix = config.get('elasticsearch_index_prefix')

headers = {
    "Content-Type": "application/json"
}

required_mapping_fields = {
    'timestamp': {'type': 'date'},
    'guid': {'type': 'keyword'}
}

mappings = {
    "kbasenarrative.narrative-4.0": {
        'name': {'type': 'text'},
        'upa': {'type': 'text'},
        'markdown_text': {'type': 'text'},
        'app_names': {'type': 'text'},
        'creator': {'type': 'text'},
        'total_cells': {'type': 'short'},
        'epoch': {'type': 'date'}
    }
}


def _create_index(index, mapping):
    """
    """
    # merge the two dictionaries (shallowly)
    # this ordering overwrites any field in 'mapping'
    # that are defined in 'required_mapping_fields'
    request_body = {
        "mappings": {
            es_data_type: {
                "properties": {**mapping, **required_mapping_fields}
            }
        },
        "settings": {
            "index": {
                "number_of_shards": 10,
                "number_of_replicas": 2
            }
        }
    }

    try:
        resp = requests.put(
            '/'.join([es_url, index]),
            data=json.dumps(request_body),
            headers=headers
        )
    except requests.exceptions.RequestException as error:
        raise error

    if not resp.ok:
        raise RuntimeError("Error while creating new index %s: " % index + resp.text +
                           ". Exited with status code %i" % resp.status_code)


def set_up_indexes():
    print("setting up indices...")
    try:
        resp = requests.get(
            es_url + "/_aliases",
        )
    except requests.exceptions.RequestException as error:
        raise error
    if not resp.ok:
        raise RuntimeError("Error while querying for indices: " + resp.text +
                           ". Exited with status code %i" % resp.status_code)
    indexes_data = resp.json()

    indexes = indexes_data.keys()
    for index, mapping in mappings.items():
        index = es_index_prefix + '.' + index + "_1"
        if index in indexes:
            print("index %s already created" % index)
            continue
        print("creating new index %s" % index)
        # create index here using the mapping stored above.
        _create_index(index, mapping)

    print("all indices loaded...")