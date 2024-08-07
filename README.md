# Imapy: IMAP for Humans

[![codecov](https://codecov.io/github/vladimarius/imapy/branch/master/graph/badge.svg?token=cumYUAsSjO)](https://codecov.io/github/vladimarius/imapy)
![GitHub Actions](https://github.com/vladimarius/imapy/actions/workflows/python-package.yml/badge.svg)


Imapy is a Python library that simplifies working with the IMAP protocol, making it more accessible and user-friendly.

## Features

- Easy-to-use interface for IMAP operations
- Support for searching and filtering emails
- Handling of email attachments
- Folder management capabilities

## Requirements

- Python 3.9 or higher

## Installation

You can install Imapy using pip:

```
pip install imapy
```

## Quick Start

```python
import imapy

# Connect to an IMAP server
em = imapy.connect(
    host='imap.example.com',
    username='your_username',
    password='your_password',
    ssl=True
)

# List all folders
folders = em.folders()

# Select a folder and get emails
emails = em.folder('Inbox').emails()

# Perform operations on emails
for email in emails:
    print(f"Subject: {email.subject}")
    print(f"From: {email.sender}")

# Logout
em.logout()
```

## Documentation

For full documentation, please visit [our documentation page](https://imapy.readthedocs.io).

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and [Black](https://github.com/psf/black) for code formatting.

To set up the development environment:

1. Ensure you have Python 3.9 or higher installed
2. Install Poetry
3. Clone the repository
4. Run `poetry install` to install dependencies
5. Run `poetry run pre-commit install` to set up the pre-commit hooks

To format the code, run:

```
poetry run format
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
