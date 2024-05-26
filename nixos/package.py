"""
TODO
"""


class Package:
    """
    TODO
    """

    def __init__(self, configuration, key: str):
        """
        TODO
        :param configuration:
        :param key:
        """
        self._configuration = configuration
        self._key = key
        self._attributes = None

    @staticmethod
    def process_attributes(attributes):
        """
        TODO
        :param attributes:
        :return:
        """
        meta = attributes["meta"]
        del attributes["meta"]
        attributes.update(meta)
        del attributes["system"]
        if "license" in attributes and attributes["license"] is list:
            attributes["license"] = attributes["license"][0] if len(attributes["license"]) > 0 else None
        attributes["license"] = attributes["license"] if "license" in attributes else None
        attributes["maintainers"] = attributes["maintainers"] if "maintainers" in attributes else []
        attributes["position"] = attributes["position"] if "position" in attributes else ""
        if attributes["position"] is str:
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
        attributes["platforms"] = filter(lambda platform: platform is str, attributes["platforms"])
        if attributes["description"] is str:
            attributes["description"] = str(attributes["description"])
        return attributes

    @property
    def attributes(self):
        """
        TODO
        :return:
        """
        if not self._attributes:
            self._attributes = Package.process_attributes(self._configuration.eval.get_package_attributes(self._key))
        return self._attributes

    @property
    def key(self):
        """
        TODO
        :return:
        """
        return self._key

    def __str__(self):
        return f'{self._key}-{self["version"]}'

    def __getitem__(self, item):
        return self.attributes[item]

    def __contains__(self, item):
        return item in self.attributes

    @property
    def name(self):
        """
        TODO
        :return:
        """
        return self.attributes["name"]

    @property
    def version(self):
        """
        TODO
        :return:
        """
        return self.attributes["version"]

    @property
    def pname(self):
        """
        TODO
        :return:
        """
        return self.attributes["pname"]

    @property
    def available(self):
        """
        TODO
        :return:
        """
        return self.attributes["available"]

    @property
    def unavailable(self):
        """
        TODO
        :return:
        """
        return not self.available

    @property
    def broken(self):
        """
        TODO
        :return:
        """
        return self.attributes["broken"]

    @property
    def working(self):
        """
        TODO
        :return:
        """
        return not self.broken

    @property
    def good(self):
        """
        TODO
        :return:
        """
        return self.working and self.secure and self.supported

    @property
    def insecure(self):
        """
        TODO
        :return:
        """
        return self.attributes["insecure"]

    @property
    def secure(self):
        """
        TODO
        :return:
        """
        return not self.insecure

    @property
    def unfree(self):
        """
        TODO
        :return:
        """
        return self.attributes["unfree"]

    @property
    def free(self):
        """
        TODO
        :return:
        """
        return not self.unfree

    @property
    def unsupported(self):
        """
        TODO
        :return:
        """
        return self.attributes["unsupported"]

    @property
    def supported(self):
        """
        TODO
        :return:
        """
        return not self.unsupported

    @property
    def description(self):
        """
        TODO
        :return:
        """
        return self.attributes["description"]

    @property
    def homepage(self):
        """
        TODO
        :return:
        """
        return self.attributes["homepage"]

    @property
    def license_short_name(self):
        """
        TODO
        :return:
        """
        if not self.attributes["license"]:
            return None
        if "shortName" not in self.attributes["license"]:
            return self.attributes["license"]["fullName"] if "fullName" in self.attributes["license"] else "Unknown"
        return self.attributes["license"]["shortName"]

    @property
    def maintainers_name(self):
        """
        TODO
        :return:
        """
        return map(lambda maintainer: maintainer["name"], self.attributes["maintainers"])

    @property
    def maintainers_github(self):
        """
        TODO
        :return:
        """
        return map(lambda maintainer: maintainer["github"],
                   filter(lambda maintainer: "github" in maintainer, self.attributes["maintainers"]))

    @property
    def platforms(self):
        """
        TODO
        :return:
        """
        return self.attributes["platforms"]

    @property
    def position(self):
        """
        TODO
        :return:
        """
        return self.attributes["position"]
