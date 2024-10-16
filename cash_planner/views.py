from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    total_income = Transaction.objects.filter(type=Transaction.INCOME).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type=Transaction.EXPENSE).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'cash_planner/transaction_list.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'cash_planner/add_transaction.html', {'form': form})