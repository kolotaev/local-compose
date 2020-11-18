JSON_SCHEMA = {
    '$id': 'https://github.com/kolotaev/local-compose.schema.json',
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
            'type': 'object',
              'patternProperties': {
                '^[a-zA-Z0-9._-]+$': {
                    '$ref': '#/definitions/service'
                },
            },
        },
    },

    'definitions': {
        'service': {
            'type': 'object',
            'required': ['run'],
            'properties': {
                'comment': {
                    'description': 'Custom comment of the service',
                    'type': 'string',
                },
                'run': {
                    'description': 'Command to run the service',
                    'type': 'string',
                },
                'build': {
                    'description': 'Command to build the service',
                    'type': 'string',
                },
                'environment': {
                    'description': 'Environment variables for command run',
                    'type': 'object',
                    'patternProperties': {
                        '.+': {
                            'type': ['string', 'number', 'null']
                        },
                    },
                    'additionalProperties': False,
                },
                'watch': {
                    'description': 'Watch files by patterns and if anything changes re-run build and run',
                    'type': 'array',
                    'items': { 'type': 'string' },
                },
                'color': {
                    'description': 'Color that is associated with service output',
                    'type': 'string',
                    'enum': [
                        'black',
                        'red',
                        'green',
                        'yellow',
                        'blue',
                        'magenta',
                        'cyan',
                        'white',
                        'bright_black',
                        'bright_red',
                        'bright_green',
                        'bright_yellow',
                        'bright_blue',
                        'bright_magenta',
                        'bright_cyan',
                        'bright_white',
                    ],
                },
            },
        },
    },
}
