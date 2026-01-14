# ui-components Specification

## Purpose
TBD - created by archiving change update-date-input-to-calendar. Update Purpose after archive.
## Requirements
### Requirement: Date Picker for Date Filtering
The system SHALL provide a calendar-based date picker for selecting the start and end dates for filtering.

#### Scenario: Selecting a date range
- **WHEN** the user interacts with the date input field
- **THEN** a calendar widget SHALL be displayed.
- **AND** the user SHALL be able to select a date from the calendar.

#### Scenario: Default date range
- **WHEN** the application loads a CSV file
- **THEN** the date pickers for the start and end dates SHALL be automatically populated with the minimum and maximum dates present in the CSV data.

### Requirement: Display Analysis Results with Currency
The system SHALL display the analysis results in a table, formatting the profit/loss value with the correct currency symbol ($ or 원) based on the data provided by the DataAnalyzer.

#### Scenario: Displaying KRW results
- **GIVEN** the DataAnalyzer returns a result with the currency type 'KRW'
- **WHEN** the results are displayed
- **THEN** the profit/loss for that stock SHALL be formatted with the '원' symbol.
- **AND** the total profit/loss in the summary statistics SHALL be formatted with the '원' symbol.

#### Scenario: Displaying USD results
- **GIVEN** the DataAnalyzer returns a result with the currency type 'USD'
- **WHEN** the results are displayed
- **THEN** the profit/loss for that stock SHALL be formatted with the '$' symbol.
- **AND** the total profit/loss in the summary statistics SHALL be formatted with the '$' symbol.

#### Scenario: Displaying Mixed Currency Results
- **GIVEN** the DataAnalyzer returns results with both 'KRW' and 'USD' currency types
- **WHEN** the results are displayed
- **THEN** each row's profit/loss SHALL be formatted with its corresponding currency symbol.
- **AND** the summary statistics SHALL display separate totals for each currency (e.g., "총 평가손익(KRW): 1,000원 | 총 평가손익(USD): $50.00").

### Requirement: Sort Analysis Results
The system SHALL allow sorting the analysis results table by clicking on the column headers.

#### Scenario: Sort by Profit/Loss
- **GIVEN** the analysis results are displayed in a table with columns including '종목명'(Stock Name) and '평가손익'(Profit/Loss).
- **WHEN** the user clicks the '평가손익' column header.
- **THEN** the table rows SHALL be sorted based on the profit/loss values in descending order.
- **AND** if the user clicks the '평가손익' column header again, the table rows SHALL be sorted in ascending order.
- **AND** this sorting functionality SHALL work correctly for all currencies, including KRW and USD.

### Requirement: Display Application Version
The system SHALL display the application's current version number in the main window.

#### Scenario: Version number is visible on launch
- **GIVEN** the application has a version number defined
- **WHEN** the user launches the application
- **THEN** the version number SHALL be clearly visible in the main UI, for instance, in a status bar or footer area.

