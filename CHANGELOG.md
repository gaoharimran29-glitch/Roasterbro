# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added the `remote` command (`-rm`) for scanning GitHub repositories by owner/repo, URL, or SSH target.
- Added optional `--ref`, `--token`, and `--json` options to remote scans.

### Changed

- Remote scans now use GitHub API metadata for repository creation date, contributors, commits, latest commit date, and branch information.
- Remote scans download a temporary snapshot instead of cloning Git history; temporary files are removed after scanning.

### Fixed

- Fixed remote contributor counts to exclude anonymous contribution records and match GitHub's visible contributor count.

### Removed

- Removed deprecated functionality.