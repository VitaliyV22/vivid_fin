from flask import Blueprint, render_template, flash, redirect, url_for,request
from flask_login import current_user, login_required
from .models import Transaction
from .forms import TransactionForm, EditTransactionForm
from . import db

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/add_transaction', methods=['GET', 'POST'])
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

@transaction_bp.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to edit this transaction.')
        return redirect(url_for('main.index'))

    form = EditTransactionForm(obj=transaction)
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.category = form.category.data
        db.session.commit()
        flash('Transaction updated successfully.')
        return redirect(url_for('main.index'))
    
    return render_template('edit_transaction.html', title='Edit Transaction', form=form, transaction_id=transaction_id)

@transaction_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.')
        return redirect(url_for('main.index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully')
    return redirect(request.referrer)


@transaction_bp.route('/', methods=['GET','POST'])
@login_required
def transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_transactions_amount = sum(transaction.amount for transaction in transactions)
    return render_template('transactions.html',title='Transactions', transactions=transactions,total_transactions_amount=total_transactions_amount)
