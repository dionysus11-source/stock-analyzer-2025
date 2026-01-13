# data-analyzer Specification

## Purpose
TBD - created by archiving change update-currency-display-based-on-code. Update Purpose after archive.
## Requirements
### Requirement: Analyze Stock Profit/Loss
The system SHALL analyze a CSV file containing stock transaction data and return aggregated profit/loss information per stock.

#### Scenario: Successful Analysis
- **WHEN** a valid CSV file path is provided
- **THEN** the system SHALL return a list of tuples, where each tuple contains the stock name, total profit/loss, and number of sell trades.

### Requirement: Currency Identification
The system SHALL identify the currency for each stock based on its '코드' (code) column.

#### Scenario: Korean Stock (KRW)
- **WHEN** the '코드' value for a stock is numeric
- **THEN** the currency for that stock SHALL be identified as 'KRW'.

#### Scenario: US Stock (USD)
- **WHEN** the '코드' value for a stock is alphabetic
- **THEN** the currency for that stock SHALL be identified as 'USD'.

### Requirement: Include Currency in Analysis Results
The system SHALL include the identified currency type in the analysis result for each stock.

#### Scenario: Analysis result format
- **WHEN** `analyze_csv` is called
- **THEN** it SHALL return a list of tuples in the format `(stock_name, profit_loss, sell_count, currency_type)`.
- **AND** `currency_type` will be a string ('KRW' or 'USD').

### Requirement: Calculate Statistics by Currency
The system SHALL calculate and provide summary statistics, aggregated by currency.

#### Scenario: Mixed Currency Statistics
- **WHEN** `get_statistics` is called after analyzing data with mixed currencies
- **THEN** it SHALL return a dictionary containing total profit/loss for each currency (e.g., `total_profit_krw`, `total_profit_usd`).

