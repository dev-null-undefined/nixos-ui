"""
TODO
"""
import os
import ujson

from nixos.evaluation import Evaluation


class CachePackagesInfoFile:
    """
    TODO
    """

    def __init__(self, configuration, generator, validator):
        self.configuration = configuration
        self.validator = validator
        self.generator = generator
        self.hashed_id = None
        self.packages_info_file_path = None
        self.package_info_data = None
        self._load_cached()

    def __regen(self):
        if self.is_valid():
            return
        self.hashed_id = self.configuration.packages_hash
        info_file_path = os.path.join(self.configuration.packages_index_folder, "packages_info.json")
        assert self.generator(info_file_path)
        self.packages_info_file_path = info_file_path
        assert self._load_file(self.packages_info_file_path)

    def get_file_path(self):
        """
        TODO
        :return:
        """
        if not self.is_valid():
            self.__regen()
            assert self.is_valid()
        return self.packages_info_file_path

    def get_file(self):
        """
        TODO
        :return:
        """
        return open(self.get_file_path(), 'r', encoding="utf-8")

    def get_data(self):
        """
        TODO
        :return:
        """
        if not self.is_valid():
            self.__regen()
            assert self.is_valid()
        return self.package_info_data

    def is_valid(self):
        """
        TODO
        :return:
        """
        return self.packages_info_file_path and self.package_info_data and self.validator(self)

    def _find_cached_file_path(self):
        for file in os.listdir(self.configuration.packages_index_folder):
            if file == "packages_info.json":
                print("Found cached file:", file)
                return os.path.join(self.configuration.packages_index_folder, file)
        return None

    def _load_file(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as package_info_file:
            try:
                self.package_info_data = ujson.load(package_info_file)
                self.packages_info_file_path = file_path
                self.hashed_id = self.configuration.packages_hash
            except ValueError:
                self.package_info_data = None
                self.packages_info_file_path = None
                return False
            return True

    def _load_cached(self):
        while file := self._find_cached_file_path():
            if self._load_file(file):
                return True
            print("Removing invalid cached file:", file)
            os.remove(file)
        return False


class CachedEvaluation(Evaluation):
    """
    This class represents the evaluation of a configuration.
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        self.packages_info_file = CachePackagesInfoFile(configuration, super()._get_packages_info_into_file_path,
                                                        self.__validate)

    def get_package_names(self):
        return super()._get_package_names_from_dict(self.packages_info_file.get_data())

    def get_package_attributes(self, package_name: str):
        return super()._get_package_attributes_from_dict(self.packages_info_file.get_data(), package_name)

    def __validate(self, cache_file: CachePackagesInfoFile):
        return cache_file.packages_info_file_path and cache_file.hashed_id == self.configuration.packages_hash
