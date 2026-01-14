# versioning Specification

## Purpose
TBD - created by archiving change add-versioning-feature. Update Purpose after archive.
## Requirements
### Requirement: Application Version
The system SHALL have a version number stored in a dedicated, easily updatable file. The version number SHOULD follow the Semantic Versioning format (e.g., `MAJOR.MINOR.PATCH`).

#### Scenario: Retrieve application version
- **GIVEN** the application is starting
- **WHEN** the version information is loaded
- **THEN** the application SHALL have access to the current version string.
- **AND** the version string SHALL be in the format "vX.Y.Z".

