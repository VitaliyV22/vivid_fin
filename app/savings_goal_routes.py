from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import SavingsGoal
from .forms import SavingsGoalForm, EditSavingsGoalForm
from . import db

savings_goal_bp = Blueprint('savings_goal', __name__)

@savings_goal_bp.route('/add_savings_goal', methods=['GET', 'POST'])
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

@savings_goal_bp.route('/edit_savings_goal/<int:savings_goal_id>', methods=['GET', 'POST'])
@login_required
def edit_savings_goal(savings_goal_id):
    savings_goal = SavingsGoal.query.get_or_404(savings_goal_id)
    if savings_goal.user_id != current_user.id:
        flash('You do not have permission to edit this savings goal.')
        return redirect(url_for('main.index'))

    form = EditSavingsGoalForm(obj=savings_goal)
    if form.validate_on_submit():
        savings_goal.goal = form.goal.data
        savings_goal.amount = form.amount.data
        savings_goal.current_amount = form.current_amount.data
        db.session.commit()
        flash('Savings goal updated successfully.')
        return redirect(url_for('main.index'))
    
    return render_template('edit_savings_goal.html', title='Edit Savings Goal', form=form, savings_goal_id=savings_goal_id)

@savings_goal_bp.route('/delete_savings_goal/<int:savings_goal_id>', methods=['POST'])
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
