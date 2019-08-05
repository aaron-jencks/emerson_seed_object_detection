from .classes import File

import json


class ConfigFile(File):
    def __init__(self, path: str):
        super().__init__(path)
        self.values = {'': {}}

    def __getitem__(self, item):
        if isinstance(item, str):
            if item not in self.values.keys():
                self.values[item] = {}

            return self.values[item]
        else:
            raise TypeError('only strings can be used as key names')

    def get_pairs(self):
        opened = False
        if not self.is_opened:
            opened = True
            self.open()

        current_section = ''
        for line in self.fp:
            if not line.startswith('#'):
                if line.startswith('['):
                    current_section = line[1:-1]
                    self.values[current_section] = {}
                else:
                    i = line.index('=')
                    key = line[:i].strip()
                    value = json.loads(line[i + 1:].strip())
                    self.values[current_section][key] = value

        if opened:
            self.close()

    def save(self):
        opened = False
        if not self.is_opened:
            opened = True
            self.open()

        target = ''
        for section in self.values:
            target += '[{}]\n'.format(section)
            for key in self.values[section]:
                target += '{}={}'.format(key, json.dumps(self.values[section][key]))
        self.fp.write(target)

        if opened:
            self.close()
