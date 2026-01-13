## ADDED Requirements
### Requirement: Date Picker for Date Filtering
The system SHALL provide a calendar-based date picker for selecting the start and end dates for filtering.

#### Scenario: Selecting a date range
- **WHEN** the user interacts with the date input field
- **THEN** a calendar widget SHALL be displayed.
- **AND** the user SHALL be able to select a date from the calendar.

#### Scenario: Default date range
- **WHEN** the application loads a CSV file
- **THEN** the date pickers for the start and end dates SHALL be automatically populated with the minimum and maximum dates present in the CSV data.
