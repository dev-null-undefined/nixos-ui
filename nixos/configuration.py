"""
Configuration
"""

from nixos.configuration_settings import ConfigurationSettings
from nixos.cached_evaluation import CachedEvaluation
from nixos.package import Package


class Configuration(ConfigurationSettings):
    """
    Conf
    """

    def __init__(self, path: str, packages_path: str = "nixpkgs", resource_manager=None):
        super().__init__(path, packages_path, resource_manager)
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
            self._packages = [Package(self, x) for x in self.eval.get_package_names()]
        return self._packages

    def set_indexer(self, indexer):
        """
        Set indexer used for searching and querying packages
        :param indexer:
        :return:
        """
        self.indexer = indexer
