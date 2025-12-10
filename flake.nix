{
  description = "My solutions for the 2025 Advent of Code challenges";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems =
        f:
        builtins.listToAttrs (
          map (name: {
            inherit name;
            value = f name;
          }) systems
        );
    in
    {
      packages = forAllSystems (
        system:
        let
          legacyPkgs = self.legacyPackages.${system};
          # Flatten the structure: day01.python -> day01-python
          flattenedPackages = builtins.listToAttrs (
            builtins.concatMap (
              dayName:
              let
                dayPkgs = legacyPkgs.${dayName};
              in
              map (lang: {
                name = "${dayName}-${lang}";
                value = dayPkgs.${lang};
              }) (builtins.attrNames dayPkgs)
            ) (builtins.attrNames legacyPkgs)
          );
        in
        flattenedPackages
      );
      formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixfmt-rfc-style);
      legacyPackages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};

          # Get all directories in the current directory
          allEntries = builtins.readDir ./.;

          # Filter for dayXX directories that contain AoC.py
          dayDirs = builtins.filter (
            name:
            let
              entry = allEntries.${name};
              isDayDir = entry == "directory" && builtins.match "day[0-9][0-9]" name != null;
              hasAoCPy = isDayDir && builtins.pathExists (./. + "/${name}/AoC.py");
            in
            hasAoCPy
          ) (builtins.attrNames allEntries);

          # Python with packages
          pythonWithPackages = pkgs.python3.withPackages (ps: with ps; [
            numpy
            scipy
          ]);

          # Create a package for each day
          makeDayPackage =
            day:
            let
              dayPath = ./. + "/${day}";
            in
            {
              python = pkgs.writeShellScriptBin day ''
                exec ${pythonWithPackages}/bin/python3 "${dayPath}/AoC.py" "${dayPath}/input.txt"
              '';
              python-test = pkgs.writeShellScriptBin day ''
                exec ${pythonWithPackages}/bin/python3 "${dayPath}/AoC.py" "${dayPath}/test.txt"
              '';
            };

          # Convert list of days into attribute set
          dayPackages = builtins.listToAttrs (
            map (day: {
              name = day;
              value = makeDayPackage day;
            }) dayDirs
          );

          new-day = pkgs.writeShellScriptBin "new-day" ''
            day_num=$(ls -d day* | wc -l)
            day_num=$(($day_num + 1))
            day_num=$(printf "%02d" $day_num)
            mkdir day$day_num
            cp -r template/* day$day_num
            git add day$day_num
            echo "Created day$day_num with AoC.py, input.txt, and test.txt"
          '';
        in
        { inherit new-day; } // dayPackages
      );
    };
}
