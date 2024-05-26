"""
TODO
"""
import os
import pickle
import subprocess
import tempfile
from hashlib import sha256

import requests
from favicon import favicon


class Favicon:
    """
    TODO
    """

    def __init__(self, url, path, file_format):
        """
        TODO
        :param url:
        :param path:
        :param file_format:
        """
        self.url = url
        self.hashed_url = sha256(url.encode()).hexdigest()
        self._resource_path = path
        self.file_format = file_format

    @property
    def path(self):
        """
        TODO
        :return:
        """
        return os.path.join(self._resource_path, self.hashed_url + ".png")

    @property
    def format_path(self):
        """
        TODO
        :return:
        """
        return self.path + "." + self.file_format


class Resources:
    """
    TODO
    """

    def __init__(self):
        self.favicons = {}
        self._other = {}

    def __str__(self):
        """
        TODO
        :return:
        """
        return f"Resources: {len(self.favicons.keys())}"

    def count_broken(self):
        """
        TODO
        :return:
        """
        return sum(1 for x in self.favicons.values() if x is None)


class ResourceManager:
    """
    TODO
    """

    def __init__(self):
        """
        TODO
        """
        self._resources = Resources()
        self._path = None
        self._resource_path = None
        self._create_temp_dir()
        self._load_resources()

    @property
    def path(self):
        """
        TODO
        :return:
        """
        return self._path

    def _create_temp_dir(self):
        path = tempfile.gettempdir()
        self._path = os.path.join(path, "nixos-ui")
        os.makedirs(self._path, exist_ok=True)
        self._resource_path = os.path.join(self._path, "resources")
        os.makedirs(self._resource_path, exist_ok=True)

    def get_favicon(self, url):
        """
        TODO
        :param url:
        :return:
        """
        if url in self._resources.favicons:
            return self._resources.favicons[url]
        try:
            self._resources.favicons[url] = self._download_favicon(url)
        except requests.exceptions.RequestException as e:
            print("Request error occurred while downloading favicon: ", e)
            self._resources.favicons[url] = None
        except FileNotFoundError as e:
            print("No favicon error occurred while downloading favicon: ", e)
            self._resources.favicons[url] = None
        except TypeError as e:
            print("Convert error occurred while downloading favicon: ", e)
            self._resources.favicons[url] = None
        self._save_resources()
        return self._resources.favicons[url]

    def _download_favicon(self, url):
        icons = favicon.get(url)
        # find icon closes to 128x128
        icons.sort(key=lambda x: abs(x.width - 128) + abs(x.height - 128))
        if len(icons) == 0:
            raise FileNotFoundError("No favicon found")
        icon = Favicon(icons[0].url, self._resource_path, icons[0].format)
        if icon.url in self._resources.favicons:
            return self._resources.favicons[icon.url]
        response = requests.get(icon.url, stream=True, timeout=5)
        tmp_path = icon.path + (("." + icon.file_format) if icon.file_format != "png" else "")
        with open(tmp_path, 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)
        if icon.file_format != "png":
            result = subprocess.run(["convert", "-density", "200", tmp_path, icon.path], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=False)
            os.remove(tmp_path)
            if result.returncode != 0:
                os.remove(icon.path)
                print(result.stderr)
                raise TypeError("Error occurred while converting favicon")
        self._resources.favicons[icon.url] = icon
        return icon

    def _load_resources(self):
        pickled_resources = os.path.join(self._resource_path, "resources.pickle")
        if not os.path.exists(pickled_resources):
            return
        with open(pickled_resources, 'rb') as file:
            self._resources = pickle.load(file)

    def _save_resources(self):
        pickled_resources = os.path.join(self._resource_path, "resources.pickle")
        with open(pickled_resources, 'wb') as file:
            pickle.dump(self._resources, file)
