import os
import pickle
import subprocess
import tempfile
from hashlib import sha256

import requests
from favicon import favicon


class Favicon:
    def __init__(self, url, path, format):
        self.url = url
        self.hashed_url = sha256(url.encode()).hexdigest()
        self._resource_path = path
        self.format = format

    @property
    def path(self):
        return os.path.join(self._resource_path, self.hashed_url + ".png")


class Resources:
    def __init__(self):
        self.favicons = {}
        self._other = {}


class ResourceManager:
    def __init__(self):
        self._resources = Resources()
        self._path = None
        self._resource_path = None
        self._create_temp_dir()
        self._load_resources()

    @property
    def path(self):
        return self._path

    def _create_temp_dir(self):
        path = tempfile.gettempdir()
        self._path = os.path.join(path, "nixos-ui")
        os.makedirs(self._path, exist_ok=True)
        self._resource_path = os.path.join(self._path, "resources")
        os.makedirs(self._resource_path, exist_ok=True)

    def get_favicon(self, url):
        if url in self._resources.favicons:
            return self._resources.favicons[url]
        try:
            self._resources.favicons[url] = self.download_favicon(url)
        except Exception as e:
            print("Error occurred while downloading favicon: ", e)
            self._resources.favicons[url] = None
        self._save_resources()
        return self._resources.favicons[url]

    def download_favicon(self, url):
        icons = favicon.get(url)
        # find icon closes to 128x128
        icons.sort(key=lambda x: abs(x.width - 128) + abs(x.height - 128))
        if len(icons) == 0:
            raise Exception("No icons found")
        icon = Favicon(icons[0].url, self._resource_path, icons[0].format)
        if icon.url in self._resources.favicons:
            return self._resources.favicons[icon.url]
        response = requests.get(icon.url, stream=True)
        tmp_path = icon.path + (("." + icon.format) if icon.format != "png" else "")
        with open(tmp_path, 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)
        if icon.format != "png":
            result = subprocess.run(["convert", "-density", "200", tmp_path, icon.path], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=False)
            os.remove(tmp_path)
            if result.returncode != 0:
                os.remove(icon.path)
                print(result.stderr)
                raise Exception("Error occurred while converting favicon")
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
