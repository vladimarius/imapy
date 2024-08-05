# Changelog

## [2.0.0] - 2024-08-05
- Dropped support for Python2
- Updated email information retrieval syntax
- Added type hints
- Added more tests

## [1.2.1] - 2023-03-06
### Added
- Added authentication support

## [1.2.0] - 2019-01-29
### Added
- Added support to only retrieve a list of UIDs

### Fixed
- Parsing bugfixes

### Changed
- Reorganize tests and use tox + Travis for CI

## [1.1.1] - 2016-01-20
### Fixed
- Add context manager to IMAP class because gremlins had stolen it from previous release

## [1.1.0] - 2015-11-22
### Added
- Add a context manager to IMAP class.
- Add port argument to IMAP.connect (in cases when non-default port is used)
- Add support for attachments
- Search for folders using simple regular expressions: `box.folders('*nbo*')` will match 'Inbox' folder
- Shorter syntax for folder creation: use `make()` instead of `make_folder()`

## [1.0.3] - 2015-05-20
### Fixed
- Couldn't parse email attributes (flags, uid) sent by a server which were coming after email contents.
- Incorrect email header parsing under Python 3 and in situations when some 'obvious' headers ('Subject', 'To') were not present in email.

## [1.0.2] - 2015-05-18
### Added
- Email headers access is case insensitive
- Text and HTML contents/attachments are now accessed via `email['text']` and `email['html']`. Before: `email['attachments']['text']` and `email['attachments']['html']`

## [1.0.1] - 2015-05-14
### Fixed
- Raised error when trying to delete currently selected folder

## [1.0.0] - 2015-05-14
### Added
- Initial release