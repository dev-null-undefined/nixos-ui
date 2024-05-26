"""
TODO
"""
import os
import subprocess
import tempfile
import ujson

from nixos.configuration_settings import ConfigurationSettings

command_template_query = [
    "nix-env",
    "--query",
    "--available",
    "--attr-path",
    "--status",
    "--json",
    "--meta",
    "--arg",
    "config",
    "{ allowAliases = false;"
    " allowUnfree = true;"
    " allowBroken = true;"
    " allowInsecurePredicate = x: true;"
    " }",
    "--file"
]

command_template_build = [
    "nix",
    "build",
    "--no-link",
    "--print-out-paths",
    "--arg",
    "config",
    "{ allowAliases = false;"
    " allowUnfree = true;"
    " allowBroken = true;"
    " allowInsecurePredicate = x: true;"
    " }",
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
        with self._get_packages_info_file() as info_file:
            path = info_file.name
            packages = self._get_package_names_from_file(info_file)
        os.unlink(path)
        return packages

    def _get_empty_packages_info_file(self):
        return tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8")

    def _get_packages_info_into_file(self, file):
        command = [*command_template_query, self.configuration.real_packages_path]
        print("Executing command: ", " ".join(command))
        result = subprocess.run(command, stdout=file, stderr=subprocess.PIPE, text=True, check=False)

        # Check for errors
        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return None

        print("Output saved to:", file.name)

        print("Compressing JSON data")
        # Compress JSON data using ujson load and immediately dump it back to the file
        with open(file.name, 'r', encoding="utf-8") as r_file:
            try:
                loaded = ujson.load(r_file)
            except ValueError:
                print("Error occurred while loading JSON data")
                return None
        with open(file.name, 'w', encoding="utf-8") as w_file:
            ujson.dump(loaded, w_file)
        print("Finished generating packages info file")
        return w_file

    def _get_packages_info_into_file_path(self, file_path):
        with open(file_path, 'w', encoding="utf-8") as file:
            return self._get_packages_info_into_file(file)

    def _get_packages_info_file(self):
        info_file = self._get_empty_packages_info_file()
        return self._get_packages_info_into_file(info_file)

    def _get_package_names_from_file(self, file):
        return self._get_package_names_from_dict(ujson.load(file))

    def _get_package_names_from_dict(self, data):
        return data.keys()

    def _get_package_attributes_from_file(self, file, package_name):
        return self._get_package_attributes_from_dict(ujson.load(file), package_name)

    def _get_package_attributes_from_dict(self, data, package_name):
        return data[package_name]

    def get_package_attributes(self, package_name: str):
        """
        This function returns the attributes of the package in the configuration.
        """
        with self._get_packages_info_file() as info_file:
            path = info_file.name
            attributes = self._get_package_attributes_from_file(info_file, package_name)
        os.unlink(path)
        return attributes

    def get_options(self):
        """
        This function returns the options of the configuration.
        """
        options = {}

        return options

    def build(self, package):
        """
        TODO
        :return:
        """
        command = [*command_template_build, self.configuration.real_packages_path,  package.key]
        print("Executing command: ", " ".join(command))
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)

        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return None

        if not result.stdout:
            print("No output from build")
            return None

        path = result.stdout.strip()
        print("Output path:", path)
        return path
