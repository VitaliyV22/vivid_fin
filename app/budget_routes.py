from flask import Blueprint, render_template, flash, redirect, url_for,request
from flask_login import current_user, login_required
from .models import Budget
from .forms import BudgetForm, EditBudgetForm
from . import db

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget(category=form.category.data, amount=form.amount.data, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Budget added successfully')
        return redirect(url_for('budget.html'))
    return render_template('add_budget.html', title='Add Budget', form=form)

@budget_bp.route('/edit_budget/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash('You do not have permission to edit this budget.')
        return redirect(url_for('main.index'))

    form = EditBudgetForm(obj=budget)
    if form.validate_on_submit():
        budget.category = form.category.data
        budget.amount = form.amount.data
        db.session.commit()
        flash('Budget updated successfully.')
        return redirect(url_for('budget.budget'))
    
    return render_template('edit_budget.html', title='Edit Budget', form=form, budget_id=budget_id)

@budget_bp.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash('You do not have permission to delete this budget.')
        return redirect(url_for('main.index'))
    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully')
    return redirect(request.referrer )


@budget_bp.route('/', methods=['GET', 'POST'])
@login_required
def budget():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template('budget.html', title='Budget', budgets=budgets, )
