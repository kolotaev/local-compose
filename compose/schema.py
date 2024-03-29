JSON_SCHEMA = {
    '$id': 'https://github.com/kolotaev/local-compose.schema.json',
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Local-compose tool schema',
    'type': 'object',

    'required': [
        'version',
    ],

    'properties': {
        'version': {
            'description': 'Version of the config file format',
            'type': 'string',
        },
        'settings': {
            'description': 'Global configuration for the tool',
            'type': 'object',
            'default': {},
            'properties': {
                'logging': {
                    '$ref': '#/definitions/logging',
                    'default': {},
                },
                'envMaps': {
                    'type': 'object',
                    'patternProperties': {
                        '^[a-zA-Z0-9._-]+$': {
                            '$ref': '#/definitions/envValuesGroup'
                        },
                    },
                },
            },
        },
        'services': {
            'description': 'List of services to run',
            'type': 'object',
            'patternProperties': {
                '^[a-zA-Z0-9._-]+$': {
                    '$ref': '#/definitions/service'
                },
            },
        },
    },

    'definitions': {
        'logging': {
            'description': 'Logging configuration',
            'type': 'object',
            'properties': {
                'timeFormat': {
                    'description': 'Time format for service output in console. Accepts strftime format',
                    'type': 'string',
                    'default': '%H:%M:%S',
                },
                'usePrefix': {
                    'description': 'Use prefix with info for service output in console?',
                    'type': 'boolean',
                    # todo - take defaults from this schema
                    'default': True,
                },
                'toStdout': {
                    'description': "Do log service's output to stdout?",
                    'type': 'boolean',
                    'default': True,
                },
                'toFile': {
                    'description': 'Output to file configuration',
                    'type': 'object',
                    'default': {},
                    'properties': {
                        'name': {
                            'description': 'Name of the file to write into',
                            'type': 'string',
                        },
                        'enabled': {
                            'description': "Enable service's output to file?",
                            'type': 'boolean',
                            'default': False,
                        },
                        'maxSize': {
                            'description': 'Maximum size in bytes file can be',
                            'type': 'integer',
                            'default': 0,
                        },
                        'count': {
                            'description': 'How many files to keep in rotating manner',
                            'type': 'number',
                            'default': 0,
                        },
                    },
                },
            },
        },
        'retry': {
            'description': 'Retry logic for re-runs, health-checks, etc.',
            'type': 'object',
            'default': {},
            'properties': {
                'attempts': {
                    'description': 'How many attempts to perform before giving up',
                    'type': 'integer',
                    'default': float('inf'),
                },
                'waitSeconds': {
                    'description': 'How many seconds to wait before the next attempt',
                    'type': 'number',
                    'default': 5,
                },
            },
        },
        'envValuesGroup': {
            'description': 'Environment variables and their corresponding values',
            'type': 'object',
            'patternProperties': {
                '.+': {
                    'type': ['string', 'number', 'null', 'boolean']
                },
            },
            'additionalProperties': False,
        },
        'service': {
            'type': 'object',
            'required': [
                'run',
            ],
            'default': {},
            'properties': {
                'comment': {
                    'description': 'Custom comment of the service',
                    'type': 'string',
                },
                'run': {
                    'description': 'Command to run the service',
                    'type': 'string',
                },
                # 'build': {
                #     'description': 'Command to build the service',
                #     'type': 'string',
                # },
                'cwd': {
                    'description': 'Current working directory to run command in',
                    'type': 'string',
                },
                'env': {
                    'description': 'Environment variables for command run',
                    '$ref': '#/definitions/envValuesGroup',
                },
                'envFromMap': {
                    'description': 'Names of the maps with the environment variables for command run',
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                    'minItems': 1,
                    'uniqueItems': True,
                },
                'envFromDotenv': {
                    'description': 'Use env variables from the .env file located in the current workdir of the service',
                    'type': 'boolean',
                    'default': False,
                },
                'envFromOS': {
                    'description': 'Use env variables from the current OS session',
                    'type': 'boolean',
                    'default': False,
                },
                # 'watch': {
                #     'description': 'Watch files by patterns and if anything changes re-run build and run',
                #     'type': 'array',
                #     'items': {
                #         'type': 'string'
                #     },
                # },
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
                'logToFile': {
                    'description': 'Service outputs are streamed into this file',
                    'type': 'string',
                },
                'readiness': {
                    'description': 'Method that can determine if service has started successfully. \
                        Currently it uses only service exit code as a probe',
                    'type': 'object',
                    'properties': {
                        'retry': {
                            '$ref': '#/definitions/retry'
                        },
                    },
                },
            },
        },
    },
}
