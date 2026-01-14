# Change: Add Application Versioning

## Why
The application currently lacks a version number, making it difficult for users to identify which version they are running and for developers to track releases. Introducing a clear versioning system will improve maintainability and user awareness.

## What Changes
- A version number (e.g., "v1.0.0") will be stored in a dedicated file.
- The application's main window will display the current version number in the UI.
- The process for updating the version for a new release will be simple and documented.

## Impact
- **Affected specs:** A new `versioning` capability will be created, and the `ui-components` capability will be modified.
- **Affected code:** 
  - `main.py`: Will read the version and pass it to the UI.
  - `ui_components.py`: Will be updated to display the version.
  - A new `_version.py` file will be created to store the version string.
