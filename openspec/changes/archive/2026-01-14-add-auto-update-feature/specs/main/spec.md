# main Specification (Change: add-auto-update-feature)

## Purpose
This document specifies the changes to the main application entry point required to support a non-blocking, user-friendly auto-update process.

## Requirements

### Requirement: Thread-Safe Update Process
The system SHALL perform the update download and preparation in a background thread to prevent the UI from freezing.

#### Scenario: Update initiated
- **GIVEN** the user has agreed to an update
- **WHEN** the update process is initiated
- **THEN** the download and preparation of the update files SHALL be executed in a background thread.
- **AND** the main UI thread SHALL remain responsive and display an `UpdateProgressDialog`.

### Requirement: Graceful Application Exit for Update
The system SHALL gracefully exit to allow the external update script to run.

#### Scenario: Update ready to be applied
- **GIVEN** the update has been successfully downloaded and prepared in a background thread
- **WHEN** the application is ready to exit and apply the update
- **THEN** the call to exit the application (`sys.exit`) SHALL be executed on the main UI thread.
- **AND** all application windows, including the `UpdateProgressDialog`, SHALL be closed as part of the exit process.
