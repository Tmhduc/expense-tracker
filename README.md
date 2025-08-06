# expense-tracker

## Description

The Expenses Tracker CLI is a Python-based command-line tool designed for users to keep track of their expenses. It utilizes the rich library to provide a user-friendly interface for managing expenses.

It is inspired from the [Expense Tracker](https://roadmap.sh/projects/expense-tracker) project featured in the [Backend Roadmap](https://roadmap.sh/backend) from [roadmap.sh](https://roadmap.sh/).

## Features

- **Add Expenses**: Add new expenses with details such as amount, category, and description
- **Delete Expenses**: Delete an expense based on its ID.
- **View Expenses**: Display a list of all recorded expenses.

## Usage

1. Run the application
   ```sh
   python expense-tracker.py add --description "Lunch" --amount 25 # Add an expense
   python expense-tracker.py add --description "Dinner" --amount 15 # Add another expense
   python expense-tracker.py list # List all expenses
   python expense-tracker.py summary # Show summary of expenses
   python expense-teacker summary --month 8 # Show summary of expenses for specific month
   python expense-tracker.py delete --id 1 # Delete an expense by ID
   ```
