from database import get_session
from utils import get_or_create_user, add_expense, set_budget, show_report as display_report


def main():
    print("Welcome to Expense & Budget Tracker")

    user_name = input("Enter your name: ")
    user_email = input("Enter your email: ")

    session_generator = get_session()
    session = next(session_generator)
    current_user = get_or_create_user(session, user_name, user_email)


    action_running = True
    while action_running:
        print("\nChoose an action:")
        print("1. Add Expense")
        print("2. Set Budget")
        print("3. Show Report")
        print("4. Exit")

        selected_option = input("Enter choice (1-4): ")

        match selected_option:
            case '1':
                expense_category = input("Category (e.g., Food, Transport): ")
                expense_amount = float(input("Amount spent: ₹"))
                expense_date = input("Date (YYYY-MM-DD): ")
                add_expense(session, current_user, expense_category, expense_amount, expense_date)

            case '2':
                budget_category = input("Category to budget: ")
                budget_month = input("Month (YYYY-MM): ")
                budget_value = float(input("Budget amount: ₹"))
                set_budget(session, current_user, budget_category, budget_month, budget_value)

            case '3':
                report_month = input("Enter month to view report (YYYY-MM): ")
                display_report(session, current_user, report_month)

            case '4':
                print("Until next time!")
                action_running = False

            case _:
                print("Invalid choice. Try again.")

    session_generator.close()


if __name__ == "__main__":
    main()
