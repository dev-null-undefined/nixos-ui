"""
Package
"""


class Package:
    def __init__(self, configuration, name: str):
        self._configuration = configuration
        self._name = name
        self._attributes = None

    @property
    def attributes(self):
        if not self._attributes:
            self._attributes = self._configuration.eval.get_package_attributes(self._name)
        return self._attributes

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f'${self._name}-${self["version"]}'

    def __getitem__(self, item):
        return self.attributes[item]

    def __contains__(self, item):
        return item in self.attributes

