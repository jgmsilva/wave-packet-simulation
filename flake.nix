{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonEnv = pkgs.python312.withPackages (ps: [
            ps.numpy
            ps.matplotlib
            ps.scipy
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = [
              pythonEnv
              # pkgs.uv
            ];

            # shellHook = ''
            #   unset PYTHONPATH
            #   uv sync
            #   . .venv/bin/activate
            # '';
          };
        }
      );
    };
}
