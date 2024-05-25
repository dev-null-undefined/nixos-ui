import subprocess
import tempfile
import json

from nixos.configuration import ConfigurationSettings

command_template = [
    "nix-env",
    "--query",
    "--available",
    "--attr-path",
    "--status",
    "--json",
    "--meta",
    "--arg",
    "config",
    "{ allowAliases = false; }",
    "--file"
]


class Evaluation:
    """
    This class represents the evaluation of a configuration.
    """

    def __init__(self, configuration: ConfigurationSettings):
        self.configuration = configuration

    def get_package_names(self):
        """
        This function returns the names of the packages in the configuration.
        """
        info_file = self._get_packages_info_file()
        return self._get_package_names_from_file(info_file)

    def _get_empty_packages_info_file(self):
        info_file = tempfile.NamedTemporaryFile(suffix=".json")
        return info_file

    def _get_packages_info_into_file(self, file):
        command = [*command_template, self.configuration.real_packages_path]
        result = subprocess.run(command, stdout=file, stderr=subprocess.PIPE, text=True, check=False)

        # Check for errors
        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return None
        else:
            print("Output saved to:", file.name)
        return file


    def _get_packages_info_into_file_path(self, file_path):
        with open(file_path, 'w') as file:
            return self._get_packages_info_into_file(file)

    def _get_packages_info_file(self):
        info_file = self._get_empty_packages_info_file()
        return self._get_packages_info_into_file(info_file)

    def _get_package_names_from_file(self, file):
        return self._get_package_names_from_dict(json.load(file))

    def _get_package_names_from_dict(self, dict):
        return dict.keys()

    def _get_package_attributes_from_file(self, file, packageName):
        return self._get_package_attributes_from_dict(json.load(file), packageName)

    def _get_package_attributes_from_dict(self, dict, packageName):
        return dict[packageName]

    def get_package_attributes(self, packageName: str):
        """
        This function returns the attributes of the package in the configuration.
        """
        info_file = self._get_packages_info_file()
        return self._get_package_attributes_from_file(info_file, packageName)

    def get_options(self):
        """
        This function returns the options of the configuration.
        """
        options = {}

        return options
