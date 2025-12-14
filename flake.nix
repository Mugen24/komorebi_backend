{
  description = "Decky auto steam";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: 
  let 
    system = "x86_64-linux";
    pkgs = import nixpkgs { 
      inherit system; 
    };
  in
  {
    devShells."${system}".default = pkgs.mkShell {
      packages = with pkgs; [
        steamcmd
      ];
      shellHook = ''
        export DEBUG=1;
        # export GAME_PATH=/home/mugen/Programing/decky_env/test_game;
        export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib;
      '';
    };
  };
}
