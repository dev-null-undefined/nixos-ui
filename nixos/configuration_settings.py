"""
TODO
"""
import os
import subprocess
from functools import cached_property
from hashlib import sha256


class ConfigurationSettings:
    """
    Configuration settings
    """

    def __init__(self, path, packages_path, resource_manager):
        self.path = path
        self.packages_path = packages_path
        self.resource_manager = resource_manager
        self.__get_real_packages_path()

    @cached_property
    def packages_hash(self):
        """
        TODO
        :return:
        """
        return sha256(self.real_packages_path.encode())

    @property
    def packages_index_folder(self):
        """
        TODO
        :return:
        """
        tmp_dir = os.path.join(self.resource_manager.path, self.packages_hash.hexdigest())
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def __get_real_packages_path(self):
        result = subprocess.run(['nix-instantiate', '--find-file', self.packages_path], capture_output=True, text=True,
                                check=False)
        if result.returncode != 0:
            raise ValueError("Error occurred:", result.stderr)
        self.real_packages_path = result.stdout.strip()
        print("Real packages path:", self.real_packages_path)
        self.__dict__.pop('packages_hash', None)  # Invalidate the cache
        return self.real_packages_path
