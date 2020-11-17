JSON_SCHEMA = {
    "$id": "https://github.com/kolotaev/local-compose.schema.json",
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Local-compose tool schema',
    'required': [
        'version',
        'global',
        'services',
    ],
    'type': 'object',
    'properties': {
        'version': {
            'description': 'Version of the config file format',
            'type': float,
        },
        'global': {
            'description': 'Global configuration for the tool',
            'type': 'object',
            'properties': {},
        },
        'services': {
            'description': 'Services to run list',
            'type': 'object',
            'properties': {},
        },
    },
}
