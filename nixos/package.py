"""
Package abstraction with lazy evaluation
"""


class Package:
    """
    Lazy evaluated package abstraction
    """

    def __init__(self, configuration, key: str):
        """
        Initialize package but do not obtain attributes
        :param configuration:
        :param key:
        """
        self._configuration = configuration
        self._key = key
        self._attributes = None

    @staticmethod
    def process_attributes(attributes):
        """
        Preprocess attributes and normalize them for indexing
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
        Get normalized attributes or return them if they are already present just return
        :return:
        """
        if not self._attributes:
            self._attributes = Package.process_attributes(self._configuration.eval.get_package_attributes(self._key))
        return self._attributes

    @property
    def key(self):
        """
        Get key of the package used for building
        :return:
        """
        return self._key

    def __str__(self):
        """
        Return string representation of the package
        :return:
        """
        return f'{self._key}-{self["version"]}'

    def __getitem__(self, item):
        return self.attributes[item]

    def __contains__(self, item):
        return item in self.attributes

    def build(self):
        """
        Build the package and return path to the out link
        :return:
        """
        return self._configuration.eval.build(self)

    @property
    def name(self):
        """
        Get package name
        :return:
        """
        return self.attributes["name"]

    @property
    def version(self):
        """
        Get package version
        :return:
        """
        return self.attributes["version"]

    @property
    def pname(self):
        """
        Get package pname
        :return:
        """
        return self.attributes["pname"]

    @property
    def available(self):
        """
        Is package available
        :return:
        """
        return self.attributes["available"]

    @property
    def unavailable(self):
        """
        Is package unavailable
        :return:
        """
        return not self.available

    @property
    def broken(self):
        """
        Is package broken
        :return:
        """
        return self.attributes["broken"]

    @property
    def working(self):
        """
        Is package working
        :return:
        """
        return not self.broken

    @property
    def good(self):
        """
        Is package good which means that it working secure and supported
        :return:
        """
        return self.working and self.secure and self.supported

    @property
    def insecure(self):
        """
        Is package insecure
        :return:
        """
        return self.attributes["insecure"]

    @property
    def secure(self):
        """
        Is package secure
        :return:
        """
        return not self.insecure

    @property
    def unfree(self):
        """
        Is package unfree
        :return:
        """
        return self.attributes["unfree"]

    @property
    def free(self):
        """
        Is package free
        :return:
        """
        return not self.unfree

    @property
    def unsupported(self):
        """
        Is package unsupported
        :return:
        """
        return self.attributes["unsupported"]

    @property
    def supported(self):
        """
        Is package supported
        :return:
        """
        return not self.unsupported

    @property
    def description(self):
        """
        Description of the package
        :return:
        """
        return self.attributes["description"]

    @property
    def homepage(self):
        """
        Home page of the package project
        :return:
        """
        return self.attributes["homepage"]

    @property
    def license_short_name(self):
        """
        Short name of the license
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
        List of maintainers real names
        :return:
        """
        return map(lambda maintainer: maintainer["name"], self.attributes["maintainers"])

    @property
    def maintainers_github(self):
        """
        List of maintainers GitHub usernames
        :return:
        """
        return map(lambda maintainer: maintainer["github"],
                   filter(lambda maintainer: "github" in maintainer, self.attributes["maintainers"]))

    @property
    def platforms(self):
        """
        Platforms on which the package is available
        :return:
        """
        return self.attributes["platforms"]

    @property
    def position(self):
        """
        File in which the package is defined
        :return:
        """
        return self.attributes["position"]
