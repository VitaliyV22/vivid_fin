from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Transaction, Budget, SavingsGoal

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    return render_template('homepage.html')

@main_bp.route('/index')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    savings_goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    total_transactions_amount = sum(transaction.amount for transaction in transactions)
    
    return render_template('index.html', transactions=transactions, budgets=budgets, savings_goals=savings_goals, total_transactions_amount=total_transactions_amount)
