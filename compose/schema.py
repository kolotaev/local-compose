JSON_SCHEMA = {
    "$id": "https://github.com/kolotaev/local-compose.schema.json",
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Local-compose tool schema',
    'type': 'object',

    'required': [
        'version',
        # 'global',
        # 'services',
    ],

    'properties': {
        'version': {
            'description': 'Version of the config file format',
            # 'type': 'float',
        },
        'global': {
            'description': 'Global configuration for the tool',
            'type': 'object',
            'properties': {},
        },
        'services': {
            'description': 'Services to run list',
            'type': 'array',
            'items': { '$ref': '#/definitions/service' }
        },
    },

    'definitions': {
        'service': {
            'type': 'object',
            'required': ['run'],
            'properties': {
                'name': {
                    'description': 'Custom name of the service to be displayed and referenced by',
                    'type': 'string',
                },
                'run': {
                    'description': 'Command to run the service',
                    'type': 'string',
                },
            },
        }
    },
}
