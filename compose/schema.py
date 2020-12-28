JSON_SCHEMA = {
    '$id': 'https://github.com/kolotaev/local-compose.schema.json',
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Local-compose tool schema',
    'type': 'object',

    'required': [
        'version',
        # 'settings',
        # 'services',
    ],

    'properties': {
        'version': {
            'description': 'Version of the config file format',
            # 'type': 'float',
        },
        'settings': {
            'description': 'Global configuration for the tool',
            'type': 'object',
            'properties': {
                'time-format': {
                    'description': 'Time format for service output in console. Accepts strftime format',
                    'type': 'string',
                },
                'use-prefix': {
                    'description': 'Use prefix with info for service output in console?',
                    'type': 'boolean',
                    'default': True,
                },
            },
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
        'retry': {
            'description': 'Retry logic for re-runs, health-checks, etc.',
            'type': 'object',
            'required': ['url'],
            'properties': {
                'attempts': {
                    'description': 'How many attempts to perform before giving up',
                    'type': 'integer',
                    'default': 'Infinite',
                },
                'waitSeconds': {
                    'description': 'How many seconds to wait before the next attempt',
                    'type': 'number',
                    'default': 5,
                },
            },
        },
        'httpCheck': {
            'description': 'Health check by HTTP request',
            'type': 'object',
            'required': ['url'],
            'properties': {
                'url': {
                    'description': 'Full URL to the health check endpoint',
                    'type': 'string',
                },
                'method': {
                    'description': 'HTTP method to make a request with',
                    'type': 'string',
                    'default': 'GET',
                },
                'statusCode': {
                    'description': 'HTTP status code of the response that is considered healthy',
                    'type': 'integer',
                    'default': 200,
                },
            },
        },
        'tcpCheck': {
            'description': 'Health check by TCP probing',
            'type': 'object',
            'required': ['url'],
            'properties': {
                'endpoint': {
                    'description': 'Full endpoint name host+port to the health check',
                    'type': 'string',
                },
            },
        },
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
                'cwd': {
                    'description': 'Current working directory to run inside',
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
                'quite': {
                    'description': 'Do not log service output to anywhere?',
                    'type': 'boolean',
                    'default': False,
                },
                'shell': {
                    'description': 'Run service in system shell?',
                    'type': 'boolean',
                    'default': False,
                },
                'color': {
                    'description': 'Color that is associated with service output',
                    'type': 'string',
                },
                'readyProbe': {
                    'description': 'Method that can determine if service has started successfully',
                    'type': 'object',
                    'properties': {
                    },
                },
            },
        },
    },
}
