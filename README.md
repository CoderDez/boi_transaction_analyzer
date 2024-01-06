# boi_transaction_analyzer
A project to analyze data for a csv file containing bank account transactions

## Details
The functionality was written to work with transaction histories that can be downloaded from Bank Accounts.

The csv format is expected to be as follows: *Date,Details,Debit,Credit,Balance*

## Features 
- Ability to filter Debits and Credits
- Display monthly Credits or Debits
- Get average monthly Credits or Debits
- Export Debits or Credits to Excel

## Installation

To use this project, you need Python installed. Clone the repository and install the required dependencies using pip:
```bash
git clone https://github.com/CoderDez/boi_transaction_analyzer.git
cd boi_transaction_analyzer
pip install -r requirements.txt
