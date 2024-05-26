"""
Package
"""


class Package:
    def __init__(self, configuration, name: str):
        self._configuration = configuration
        self._name = name
        self._attributes = None

    @staticmethod
    def process_attributes(attributes):
        meta = attributes["meta"]
        del attributes["meta"]
        attributes.update(meta)
        del attributes["system"]
        if "license" in attributes and type(attributes["license"]) == list:
            attributes["license"] = attributes["license"][0] if len(attributes["license"]) > 0 else None
        attributes["license"] = attributes["license"] if "license" in attributes else None
        attributes["maintainers"] = attributes["maintainers"] if "maintainers" in attributes else []
        attributes["position"] = attributes["position"] if "position" in attributes else ""
        if type(attributes["position"]) != str:
            attributes["position"] = str(attributes["position"])
        attributes["platforms"] = attributes["platforms"] if "platforms" in attributes else []
        attributes["homepage"] = attributes["homepage"] if "homepage" in attributes else ""
        attributes["available"] = attributes["available"] if "available" in attributes else False
        attributes["broken"] = attributes["broken"] if "broken" in attributes else True
        attributes["insecure"] = attributes["insecure"] if "insecure" in attributes else True
        attributes["unfree"] = attributes["unfree"] if "unfree" in attributes else True
        attributes["unsupported"] = attributes["unsupported"] if "unsupported" in attributes else True
        attributes["description"] = attributes["description"] if "description" in attributes else True
        attributes["platforms"] = attributes["platforms"] if "platforms" in attributes else []
        attributes["platforms"] = filter(lambda platform: type(platform) == str, attributes["platforms"])
        if type(attributes["description"]) != str:
            attributes["description"] = str(attributes["description"])
        return attributes

    @property
    def attributes(self):
        if not self._attributes:
            self._attributes = Package.process_attributes(self._configuration.eval.get_package_attributes(self._name))
        return self._attributes

    @property
    def name(self):
        """
        TODO
        :return:
        """
        return self._name

    def __str__(self):
        return f'{self._name}-{self["version"]}'

    def __getitem__(self, item):
        return self.attributes[item]

    def __contains__(self, item):
        return item in self.attributes

    @property
    def name(self):
        return self.attributes["name"]

    @property
    def version(self):
        return self.attributes["version"]

    @property
    def pname(self):
        return self.attributes["pname"]

    @property
    def available(self):
        return self.attributes["available"]

    @property
    def unavailable(self):
        return not self.available

    @property
    def broken(self):
        return self.attributes["broken"]

    @property
    def working(self):
        return not self.broken

    @property
    def good(self):
        return self.working and self.secure and self.supported

    @property
    def insecure(self):
        return self.attributes["insecure"]

    @property
    def secure(self):
        return not self.insecure

    @property
    def unfree(self):
        return self.attributes["unfree"]

    @property
    def free(self):
        return not self.unfree

    @property
    def unsupported(self):
        return self.attributes["unsupported"]
    @property
    def supported(self):
        return not self.unsupported

    @property
    def description(self):
        return self.attributes["description"]

    @property
    def homepage(self):
        return self.attributes["homepage"]

    @property
    def license_short_name(self):
        if not self.attributes["license"]:
            return None
        if "shortName" not in self.attributes["license"]:
            return self.attributes["license"]["fullName"] if "fullName" in self.attributes["license"] else "Unknown"
        return self.attributes["license"]["shortName"]

    @property
    def maintainers_name(self):
        return map(lambda maintainer: maintainer["name"], self.attributes["maintainers"])

    @property
    def maintainers_github(self):
        return map(lambda maintainer: maintainer["github"], filter(lambda maintainer: "github" in maintainer, self.attributes["maintainers"]))

    @property
    def platforms(self):
        return self.attributes["platforms"]

    @property
    def position(self):
        return self.attributes["position"]
