from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import db
from .models import User, Transaction, Budget, SavingsGoal
from .forms import LoginForm, RegistrationForm, TransactionForm, BudgetForm, SavingsGoalForm
from werkzeug.urls import url_parse
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def homepage():
    return render_template('homepage.html')

@bp.route('/index')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    savings_goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', transactions=transactions, budgets=budgets, savings_goals=savings_goals)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.homepage'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(amount=form.amount.data, category=form.category.data, user_id=current_user.id)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully')
        return redirect(url_for('main.index'))
    return render_template('add_transaction.html', title='Add Transaction', form=form)

@bp.route('/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget(category=form.category.data, amount=form.amount.data, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Budget added successfully')
        return redirect(url_for('main.index'))
    return render_template('add_budget.html', title='Add Budget', form=form)

@bp.route('/add_savings_goal', methods=['GET', 'POST'])
@login_required
def add_savings_goal():
    form = SavingsGoalForm()
    if form.validate_on_submit():
        savings_goal = SavingsGoal(goal=form.goal.data, amount=form.amount.data, user_id=current_user.id)
        db.session.add(savings_goal)
        db.session.commit()
        flash('Savings Goal added successfully')
        return redirect(url_for('main.index'))
    return render_template('add_savings_goal.html', title='Add Savings Goal', form=form)

@bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.')
        return redirect(url_for('main.index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully')
    return redirect(url_for('main.index'))

@bp.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash('You do not have permission to delete this budget.')
        return redirect(url_for('main.index'))
    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully')
    return redirect(url_for('main.index'))

@bp.route('/delete_savings_goal/<int:savings_goal_id>', methods=['POST'])
@login_required
def delete_savings_goal(savings_goal_id):
    savings_goal = SavingsGoal.query.get_or_404(savings_goal_id)
    if savings_goal.user_id != current_user.id:
        flash('You do not have permission to delete this savings goal.')
        return redirect(url_for('main.index'))
    db.session.delete(savings_goal)
    db.session.commit()
    flash('Savings goal deleted successfully')
    return redirect(url_for('main.index'))