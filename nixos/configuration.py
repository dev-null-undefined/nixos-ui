"""
Configuration
"""

from nixos.configuration_settings import ConfigurationSettings
from nixos.cached_evaluation import CachedEvaluation
from nixos.package import Package

# TODO: whoosh indexing
class Configuration(ConfigurationSettings):
    """
    Conf
    """

    def __init__(self, path: str, packages_path: str = "nixpkgs"):
        super().__init__(path, packages_path)
        self.path = path
        self.eval = CachedEvaluation(self)
        self._packages = []
        self.indexer = None

    @property
    def packages(self):
        """
        TODO
        :return:
        """
        if not self._packages:
            self._packages = [ Package(self, x) for x in self.eval.get_package_names()]
        return self._packages

    def set_indexer(self, indexer):
        self.indexer = indexer
