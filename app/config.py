import yaml

class Config:
    @staticmethod
    def parse(filename):
        with open(filename) as file:
            try:
                data = yaml.parse(filename)
                return data
            except Exception as e:
                print('Config file is malformed. Error: %s' % e)
                return None
