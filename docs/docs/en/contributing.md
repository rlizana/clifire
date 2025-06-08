# Contribute to CliFire

Thank you for your interest in contributing to CliFire!

Contributions are welcome and help improve this minimalistic project designed to build CLI applications in Python.

## How to Contribute

There are several ways you can help:

- **Reporting Bugs:** If you find a bug or unexpected behavior, please open an *issue* on GitHub with a detailed description and, if possible, steps to reproduce it.
- **Requesting New Features:** If you have an idea to improve CliFire, open an *issue* or propose a *pull request*.
- **Code and Improvements:** If you wish to submit code, make sure you follow the project's style guidelines and add unit tests to support your changes.
- **Documentation:** Help improve the documentation by correcting errors, expanding sections, or adding usage examples.

## Contribution Workflow

#### **Fork the Repository**
   Fork the project on GitHub.

#### **Clone your fork locally:**
   ```bash
   git clone https://github.com/your-user/clifire.git
   cd clifire
   ```

#### **Create a Branch for your Changes:**
   ```bash
   git checkout -b my-changes
   ```

#### **Make your Changes:**

   Make the necessary changes in the code. Ensure that:

   * You follow the project's style guidelines.
   * You add unit tests—the project has 100% coverage!
   * You update or add documentation where necessary.

#### **Run the Tests:**
   Make sure all tests pass using:
   ```bash
   poetry run pytest
   ```
   Check the coverage with:
   ```bash
   poetry run coverage run -m pytest && poetry run coverage html
   ```

   You can also use `poetry run fire coverage` to run the tests and generate the coverage report.

#### **Submit a Pull Request:**
   Once you are satisfied with your changes, submit a *pull request* to the main branch of the repository. Describe in detail what you have changed and the motivation behind it.

## Best Practices

- Write clear and descriptive *commit* messages.
- Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format to document your changes.
- Ensure that new features or fixes do not break existing compatibility.
- Respect the format and structure of the existing documentation.

## Review and Feedback

Your *pull request* will be reviewed by the project maintainers. They may ask for adjustments or clarifications, so please pay close attention to any comments!

---

For further details, refer to the [Complete Contribution Guide](CONTRIBUTING.md) in the repository.

Thank you for helping CliFire grow and improve!
