{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      python-packages = ps:
        with ps; [
          pylint
          whoosh
          ujson
          pyqt5
          pyqt5-stubs
        ];
      my-python = pkgs.python311.withPackages python-packages;
    in {
      devShells.default = my-python.env;
      packages = pkgs // {custom-python = my-python;};
    });
}
