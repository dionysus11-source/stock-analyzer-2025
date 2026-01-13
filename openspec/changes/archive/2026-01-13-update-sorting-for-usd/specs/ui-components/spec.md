## ADDED Requirements
### Requirement: Sort Analysis Results
The system SHALL allow sorting the analysis results table by clicking on the column headers.

#### Scenario: Sort by Profit/Loss
- **GIVEN** the analysis results are displayed in a table with columns including '종목명'(Stock Name) and '평가손익'(Profit/Loss).
- **WHEN** the user clicks the '평가손익' column header.
- **THEN** the table rows SHALL be sorted based on the profit/loss values in descending order.
- **AND** if the user clicks the '평가손익' column header again, the table rows SHALL be sorted in ascending order.
- **AND** this sorting functionality SHALL work correctly for all currencies, including KRW and USD.
