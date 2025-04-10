from datetime import datetime
from sqlalchemy.orm import Session
from models import Expense, Budget, User
from tabulate import tabulate as format_table


def get_or_create_user(db: Session, name: str, email: str):
    existing_user = db.query(User).filter_by(email=email).first()
    if existing_user is None:
        new_user = User(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    return existing_user


def add_expense(db: Session, user: User, category: str, amount: float, date_str: str):
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    new_expense = Expense(user_id=user.id, category=category, amount=amount, date=parsed_date)
    db.add(new_expense)
    db.commit()
    print(f"Added expense of ₹{amount} in '{category}' on {date_str}")


def set_budget(db: Session, user: User, category: str, month: str, amount: float):
    existing_budget = db.query(Budget).filter_by(user_id=user.id, category=category, month=month).first()
    if existing_budget:
        existing_budget.amount = amount
    else:
        new_budget = Budget(user_id=user.id, category=category, month=month, amount=amount)
        db.add(new_budget)
    db.commit()
    print(f"Budget set: ₹{amount} for '{category}' in {month}")


def show_report(db: Session, user: User, month: str):
    print(f"\nSpending Report for {month}")
    category_rows = db.query(Expense.category).distinct().all()
    category_list = [item[0] for item in category_rows]

    report_data = []
    index = 0
    while index < len(category_list):
        current_category = category_list[index]
        category_expenses = db.query(Expense).filter(
            Expense.user_id == user.id,
            Expense.category == current_category,
            Expense.date.like(f"{month}-%")
        ).all()

        total_spent_amount = 0
        for exp in category_expenses:
            total_spent_amount += exp.amount

        budget_entry = db.query(Budget).filter_by(
            user_id=user.id,
            category=current_category,
            month=month
        ).first()

        monthly_budget = budget_entry.amount if budget_entry else 0.0

        if total_spent_amount > monthly_budget:
            budget_status = "Exceeded"
        else:
            budget_status = "Within Budget"
            if total_spent_amount > 0.9 * monthly_budget:
                budget_status = "90% Used"

        report_data.append([
            current_category,
            f"₹{total_spent_amount:.2f}",
            f"₹{monthly_budget:.2f}",
            budget_status
        ])
        index += 1

    print(format_table(report_data, headers=["Category", "Spent", "Budget", "Status"]))
