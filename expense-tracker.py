import argparse
from datetime import datetime
from utils.utils import read_expenses, write_expenses, get_month_text
from rich import print
from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser(description="Expense Tracker CLI")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Adding a subparser for the 'add' command
parser_add = subparsers.add_parser("add", help="Add a new expense")
parser_add.add_argument("--category", type=str, help="Category of the expense")
parser_add.add_argument("--description", type=str, help="Description of the expense")
parser_add.add_argument("--amount", type=float, help="Amount of the expense")

# Adding a subparser for the 'list' command
parser_list = subparsers.add_parser("list", help="List all expenses")

# Adding a subparser for the 'delete' command
parser_delete = subparsers.add_parser("delete", help="Delete an expense")
parser_delete.add_argument(
    "--id", type=int, required=True, help="ID of the expense to delete"
)

# Adding a subparser for the 'summary' command
parser_summary = subparsers.add_parser("summary", help="Show summary of expenses")
parser_summary.add_argument(
    "--month",
    type=int,
    help="Month for which to show the summary (1-12)",
    required=False,
)

# parsing the arguments
args = parser.parse_args()


# Adding an expense to the list
def add_expense(description, amount, category=None):
    if amount <= 0:
        print("Amount must be [bold green]greater[/bold green] than 0.")
        return
    try:
        amount = float(amount)
        if round(amount, 2) != amount:
            print(
                "Amount must be [bold green]rounded[/bold green] to 2 decimal places."
            )
            return
    except ValueError as e:
        print(f"[bold red]{e}[/bold red]")
        return
    expenses = read_expenses()

    if len(expenses) == 0:
        expense_id = 1
    else:
        expense_id = expenses[-1]["id"] + 1

    expenses.append(
        {
            "id": expense_id,
            "description": description,
            "amount": amount,
            "date": datetime.now().isoformat(),
            "category": category if category else "Uncategorized",
        }
    )
    write_expenses(expenses)
    print(f"Expense [bold green]added[/bold green] successfully (ID: {expense_id})")


# Listing all expenses
def list_expenses():
    expenses = read_expenses()
    if not expenses:
        print("[bold red]No expenses found.[/bold red]")
        return
    table = Table(show_header=True, title="Expenses", header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Description", style="cyan")
    table.add_column("Amount", style="green")
    table.add_column("Date", style="yellow")

    for expense in expenses:
        date = datetime.fromisoformat(expense["date"]).strftime("%Y-%m-%d %H:%M:%S")
        table.add_row(
            str(expense["id"]),
            expense["description"],
            f"${expense["amount"]:.2f}",
            date,
        )
    console = Console()

    console.print(table)


# Deleting an expense
def delete_expense(expense_id):
    expenses = read_expenses()
    if not expenses:
        print("[bold red]No expenses found to delete.[/bold red]")
        return

    if not any(expense["id"] == expense_id for expense in expenses):
        print(f"[bold red]Expense with ID {expense_id} not found.[/bold red]")
        return

    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    write_expenses(expenses)
    print(
        f"Expense with ID [bold green]{expense_id}[/bold green] deleted successfully."
    )


# Summary of expenses for a specific month or all expenses
def summary_expense(month=None):
    expenses = read_expenses()
    if not expenses:
        print("[bold red]No expenses found for summary.[/bold red]")
        return
    if len(expenses) == 0:
        print("[bold red]No expenses found.[/bold red]")
        return

    month_in_text = ""
    if month:
        month_in_text = f"for {get_month_text(month)}"
        expenses = [
            expense
            for expense in expenses
            if datetime.fromisoformat(expense["date"]).month == month
        ]
        total_amount = sum(expense["amount"] for expense in expenses)
        print(
            f"Total expenses {month_in_text}: [bold green]${total_amount:.2f}[/bold green]"
        )
        return

    total_amount = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses: [bold green]${total_amount:.2f}[/bold green]")


match args.command:
    case "add":
        add_expense(args.description, args.amount, args.category)
    case "summary":
        summary_expense(args.month)
    case "list":
        list_expenses()
    case "delete":
        delete_expense(args.id)
