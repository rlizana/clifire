# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2025-07-07

### Added

### Changed
- Minimum Python version is now 3.6.
- Remove packages version in `pyproject.toml` to use the latest versions.

### Fixed
- Change poetry to rye in the scripts for building and testing the package.

## [0.1.7] - 2025-07-06

### Added
- Add `get`, `set`, and `contains` methods to the `Config` class so that it works like a dictionary.
- Global options `--help` and `-h` to display command help
- Add `extra_args` to `Commands` with the extra arguments that are passed
- Add `query_get`, `query_set`, and `query_del` methods to the `Config` class to allow get, set, and delete operations on the configuration using `.` to navigate through configuration attributes.
- Added the `ask` method to `out` for interactive user prompts.
- Added the `path` method to `template` to obtain the absolute path of a template file.
- New global option `--no-ansi` to disable ANSI color codes in the output.
- Improved exception output to display the full traceback.
- Create `live` method in `out` to ensure only one instance of `LiveText` exists.
- Add new `add_commands` method to the `Application` class to add multiple commands.
- When use `shell` method of the `Application` class, if set a path register it is logged in the debug.

### Changed
- Improved the `LiveText` class from `out` to ensure that all created `LiveText` instances are canceled at program exit using the `atexit` library.
- Improved the `LiveText` class from `out` to expose the elapsed time since the object was created in an `elapsed_time` variable.
- Modified the `init` command so that it is executed immediately after its constructor, as it did not make sense to call it before the execution of the `fire` method since there was no code in between.
- Modified the `table` method of the `out` class to accept an optional `style` argument that allows defining the table style. If not specified, the default style is used.

### Fixed
- When using the `shell` method of the `Application` class with a specific path, after execution it ensures to return to the previous path.
- The installation of the global bash script command `fire` previously required running `cd` to launch it. Now, it no longer performs `cd`, so when the `fire` command is executed, it reads the user's current directory. The command is installed with `fire install`.
- Fixed the `help` command so that options with underscores `_` are displayed with hyphens `-` in the help output.
- Sorted the output of "Available Commands" section in the `help` command so that they appear in alphabetical order.
- When executing a group of commands, it shows the help only for the group, not the complete help.
- In the global options, the underscore `_` is not replaced by a hyphen `-` in the help output.
- Clean the command line before processing it to obtain the global options.


### Removed


## [0.1.6] - 2025-06-17

### Added

### Changed
- Code style changes and improvements: switched double quotes `"` to single quotes `'` in strings.
- Code style changes and improvements: added to pre-commit to update the main version based on `pyproject.toml`.
- Code style changes and improvements: move `clifire` package to `src` directory for better package structure.

### Fixed
- Fixed badge in README.md for the CI GitHub Actions workflow.

### Removed


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
