# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-06-17

### Added

### Changed
- Switched the package manager from `poetry` to `rye`, which is lighter and faster.

### Fixed
- Add `pyyaml` lib  to pyproject.toml dependencies.

### Removed

## [0.1.4] - 2025-06-15

### Added
- Add searching in parent directories for the `fire` command.
- Display help with available commands when a recognized group name is entered.

### Changed
- Converted the `shell` and `path` methods of the `Application` class to class methods.

### Fixed
- Fixed an execution issue when loading a command with the `@fire.command` decorator and the command does not have a `__doc__` attribute.

### Removed

## [0.1.3] - 2025-06-11

### Added
- Add `cancel` method in out.LiveText for canceling the live text output.

### Changed

### Fixed
- Fixed the decorator `@fire.command` to correctly handle commands without a docstring.

### Removed

## [0.1.2] - 2025-06-10

### Added

### Changed
- Change `out.critical` by default error code is 1

### Fixed
- Fixed the decorator `@fire.command` to correctly handle commands without a docstring.

### Removed

## [0.1.1] - 2025-06-07

### Added
- Bash command `clifire`  for creating dynamic commands.
- In application module, added:
  - Global option `--verbose` created by default.
  - If no command is passed, help is shown if the help command is defined.
  - New `path` method for get absolute path to a filename.
  - New `config` variable for managing configuration settings.
  - New `template` variable for creating files with jinja2.
- In out module, added:
  - `debug` method for printing debug messages.
  - `debug2` method for printing debug messages level 2.
  - `var_dump` method for printing pretty variables in out module.
- New `Config` class to manage configuration settings.
- New `Template` class for creating files with jinja2.
- Changed relative imports to module imports for better compatibility.

### Changed
- Commands now use `fire()` method instead of `run()`.
- Compatibility with Python 3.10.
- Updated documentation to include usage examples for the new `clifire` command.
- Enhanced the `--verbose` option to provide more detailed output during command execution.
- Improved Result class, stdout and stderr are now str instead of list

### Fixed
- The arguments between quotes are now correctly parsed, allowing for spaces in arguments.
- The [options] message in `help` command not correctly displayed.

### Removed

## [0.1.0] - 2025-06-01

### Added
- Initial release with the first usable version.
