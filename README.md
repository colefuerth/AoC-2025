# Advent of Code 2025

I am doing this year with python and nix!

## Running the problem for a day

```bash
nix run .#day01.python
```

## Testing a problem for a day

```bash
nix run .#day01.python-test
```

## Making a new day

Finds the next enumeration of folders in the format `day\d\d`, and creates it from the `template` folder.

```bash
nix run .#new-day
```
