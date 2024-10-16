from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import MainCategory, SubCategory, Source, Expense, Income, Patience
from .forms import MainCategoryForm, SubCategoryForm, SourceForm, ExpenseForm, IncomeForm, PatienceForm
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from datetime import datetime, timedelta
import csv
from .models import UserInfo


# 現在の月の最初の日と最後の日を取得する関数
def get_current_month():
    today = datetime.today()
    first_day = today.replace(day=1)  # 今月の最初の日
    last_day = today.replace(day=28) + timedelta(days=4)  # 来月の日付を計算して今月の最終日を取得
    last_day = last_day - timedelta(days=last_day.day)
    return first_day, last_day

# ホームページ（ダッシュボード）の表示
def index(request):
    # 今月の開始日と終了日を取得
    first_day, last_day = get_current_month()
    
    # 今月の支出を集計
    total_expense = Expense.objects.filter(date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 今月の収入を集計
    total_income = Income.objects.filter(date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0

    # 合計支出と合計収入をコンテキストに渡す
    context = {
        'total_expense': total_expense,
        'total_income': total_income,
    }
    return render(request, 'budget/index.html', context)

# ホームページにリダイレクトする関数
def redirect_index(request):
    return redirect(index)

# 支出を追加する機能
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ExpenseForm()
    return render(request, 'budget/add_expense.html', {'form': form})

# 支出リストの表示
def expense_list(request):
    # URLパラメータから月を取得、無ければ現在の月を使用
    month = request.GET.get('month')
    if month:
        current_date = datetime.strptime(month, '%Y-%m')
    else:
        current_date = datetime.now()

    # 月の最初の日と最後の日を計算
    first_day = current_date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # 指定された月の支出データを取得
    expenses = Expense.objects.filter(date__range=[first_day, last_day])

    # 前月と次月のためのパラメータを計算
    previous_month = (first_day - timedelta(days=1)).strftime('%Y-%m')
    next_month = (last_day + timedelta(days=1)).strftime('%Y-%m')

    context = {
        'expenses': expenses,
        'current_month': current_date.strftime('%Y年%m月'),
        'current_year': current_date.year,  # 追加
        'current_month_number': current_date.month,  # 追加
        'previous_month': previous_month,
        'next_month': next_month,
    }
    return render(request, 'budget/expense_list.html', context)

# 支出データの編集
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'budget/edit_expense.html', {'form': form})

# 支出データの削除
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'budget/delete_expense.html', {'expense': expense})

# 収入を追加する機能
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = IncomeForm()
    return render(request, 'budget/add_income.html', {'form': form})

# 収入リストの表示
def income_list(request):
    # URLパラメータから月を取得、無ければ現在の月を使用
    month = request.GET.get('month')
    if month:
        current_date = datetime.strptime(month, '%Y-%m')
    else:
        current_date = datetime.now()

    # 月の最初の日と最後の日を計算
    first_day = current_date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # 指定された月の収入データを取得
    incomes = Income.objects.filter(date__range=[first_day, last_day])

    # 前月と次月のためのパラメータを計算
    previous_month = (first_day - timedelta(days=1)).strftime('%Y-%m')
    next_month = (last_day + timedelta(days=1)).strftime('%Y-%m')

    context = {
        'incomes': incomes,
        'current_month': current_date.strftime('%Y年%m月'),
        'previous_month': previous_month,
        'next_month': next_month,
    }
    return render(request, 'budget/income_list.html', context)


# その他、ログイン関連の関数は削除

# 収入データを編集する関数
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')  # 編集後にリストページへリダイレクト
    else:
        form = IncomeForm(instance=income)
    
    return render(request, 'budget/edit_income.html', {'form': form})

    # 収入データを削除する関数
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        income.delete()  # 収入データを削除
        return redirect('income_list')  # 削除後に収入リストページへリダイレクト
    
    return render(request, 'budget/delete_income.html', {'income': income})

    # Patience（スマートセーブ）を追加する関数
def add_patience(request):
    if request.method == 'POST':
        form = PatienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patience_list')  # 追加後にリストページへリダイレクト
    else:
        form = PatienceForm()
    
    return render(request, 'budget/add_patience.html', {'form': form})

def patience_list(request):
    patiences = Patience.objects.all()  # すべてのPatienceデータを取得
    return render(request, 'budget/patience_list.html', {'patiences': patiences})

def edit_patience(request, pk):
    patience = get_object_or_404(Patience, pk=pk)
    if request.method == 'POST':
        form = PatienceForm(request.POST, instance=patience)
        if form.is_valid():
            form.save()
            return redirect('patience_list')
    else:
        form = PatienceForm(instance=patience)
    return render(request, 'budget/edit_patience.html', {'form': form})

def delete_patience(request, pk):
    patience = get_object_or_404(Patience, pk=pk)
    if request.method == 'POST':
        patience.delete()
        return redirect('patience_list')
    return render(request, 'budget/delete_patience.html', {'patience': patience})

# 支出データのグラフを表示する関数
def expense_graph(request, year, month):
    # 指定された年月の初日と末日を取得
    start_date = datetime(year, month, 1)
    next_month = start_date.replace(day=28) + timedelta(days=4)  # 翌月1日を取得
    end_date = next_month - timedelta(days=next_month.day)  # 当月末日を取得

    # 支出データを取得
    expenses = Expense.objects.filter(date__range=[start_date, end_date])

    # 日別の支出合計を計算
    daily_totals = {}
    for expense in expenses:
        date = expense.date
        amount = float(expense.amount)
        if date in daily_totals:
            daily_totals[date] += amount
        else:
            daily_totals[date] = amount

    # 日付と金額のリストを作成
    dates = list(daily_totals.keys())
    amounts = list(daily_totals.values())

    # グラフを作成
    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-', color='b')
    plt.title(f'{year}年{month}月の支出')
    plt.xlabel('日付')
    plt.ylabel('金額')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gcf().autofmt_xdate()

    # 画像をバッファに保存
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


# メインカテゴリーを追加する関数
def add_main_category(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_category_list')  # 追加後にメインカテゴリーリストページへリダイレクト
    else:
        form = MainCategoryForm()
    
    return render(request, 'budget/add_main_category.html', {'form': form})

# メインカテゴリーのリストを表示する関数
def main_category_list(request):
    categories = MainCategory.objects.all()  # 全てのメインカテゴリーを取得
    return render(request, 'budget/main_category_list.html', {'categories': categories})

# メインカテゴリーを編集する関数
def edit_main_category(request, pk):
    category = get_object_or_404(MainCategory, pk=pk)  # 主キー（pk）でカテゴリーを取得
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  # フォームが有効なら保存
            return redirect('main_category_list')  # 保存後にリストページへリダイレクト
    else:
        form = MainCategoryForm(instance=category)  # 現在のカテゴリーをフォームに表示

    return render(request, 'budget/edit_main_category.html', {'form': form})

# メインカテゴリーを削除する関数
def delete_main_category(request, pk):
    category = get_object_or_404(MainCategory, pk=pk)  # 指定された主キー（pk）でカテゴリーを取得
    if request.method == 'POST':
        category.delete()  # POSTリクエスト時に削除
        return redirect('main_category_list')  # 削除後にリストページにリダイレクト
    return render(request, 'budget/delete_main_category.html', {'category': category})

# サブカテゴリーを追加する関数
def add_sub_category(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sub_category_list')  # 追加後にサブカテゴリーリストページへリダイレクト
    else:
        form = SubCategoryForm()
    
    return render(request, 'budget/add_sub_category.html', {'form': form})

# サブカテゴリーのリストを表示する関数
def sub_category_list(request):
    subcategories = SubCategory.objects.all()  # 全てのサブカテゴリーを取得
    return render(request, 'budget/sub_category_list.html', {'subcategories': subcategories})

# サブカテゴリーを編集する関数
def edit_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)  # 指定されたサブカテゴリーを取得
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=sub_category)
        if form.is_valid():
            form.save()  # フォームが有効なら保存
            return redirect('sub_category_list')  # 保存後、サブカテゴリーリストページへリダイレクト
    else:
        form = SubCategoryForm(instance=sub_category)  # 現在のサブカテゴリーをフォームに表示
    
    return render(request, 'budget/edit_sub_category.html', {'form': form})

# サブカテゴリーを削除する関数
def delete_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)  # 指定されたサブカテゴリーを取得
    if request.method == 'POST':
        sub_category.delete()  # POSTリクエスト時に削除
        return redirect('sub_category_list')  # 削除後にサブカテゴリーリストページへリダイレクト
    return render(request, 'budget/delete_sub_category.html', {'sub_category': sub_category})

# Source（収入元など）を追加する関数
def add_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('source_list')  # 追加後、収入元リストページにリダイレクト
    else:
        form = SourceForm()
    
    return render(request, 'budget/add_source.html', {'form': form})

# Source（収入元）のリストを表示する関数
def source_list(request):
    sources = Source.objects.all()  # すべてのSourceデータを取得
    return render(request, 'budget/source_list.html', {'sources': sources})

# Source（収入元）を編集する関数
def edit_source(request, pk):
    source = get_object_or_404(Source, pk=pk)  # 指定されたSourceを取得
    if request.method == 'POST':
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()  # フォームが有効なら保存
            return redirect('source_list')  # 保存後に収入元リストページへリダイレクト
    else:
        form = SourceForm(instance=source)  # 現在のSource情報をフォームに表示
    
    return render(request, 'budget/edit_source.html', {'form': form})

# Source（収入元）を削除する関数
def delete_source(request, pk):
    source = get_object_or_404(Source, pk=pk)  # 指定されたSourceを取得
    if request.method == 'POST':
        source.delete()  # POSTリクエスト時に削除
        return redirect('source_list')  # 削除後に収入元リストページにリダイレクト
    return render(request, 'budget/delete_source.html', {'source': source})

# 支出データをCSVとしてエクスポートする関数
def export_expense_csv(request):
    # HTTPレスポンスとしてCSVを返す
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    
    # CSVライターを設定
    writer = csv.writer(response)
    writer.writerow(['日付', 'カテゴリ', 'サブカテゴリ', '金額', '支払方法', 'メモ'])

    # 支出データを取得してCSVに書き込む
    expenses = Expense.objects.all()
    for expense in expenses:
        writer.writerow([expense.date, expense.main_category.name, expense.sub_category.name if expense.sub_category else '', expense.amount, expense.payment_method, expense.description])

    return response

# 収入データをCSVとしてエクスポートする関数
def export_income_csv(request):
    # HTTPレスポンスとしてCSVを返す
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="income.csv"'

    # CSVライターを設定
    writer = csv.writer(response)
    writer.writerow(['日付', '収入元', '金額'])

    # 収入データを取得してCSVに書き込む
    incomes = Income.objects.all()
    for income in incomes:
        writer.writerow([income.date, income.source.name if income.source else '', income.amount])

    return response

# スマートセーブ（Patienceデータ）をCSVとしてエクスポートする関数
def export_smart_save_csv(request):
    # HTTPレスポンスとしてCSVを返す
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="smart_save.csv"'

    # CSVライターを設定
    writer = csv.writer(response)
    writer.writerow(['日付', 'メインカテゴリー', 'サブカテゴリー', '金額', 'メモ'])

    # スマートセーブデータを取得してCSVに書き込む
    smart_saves = Patience.objects.all()
    for save in smart_saves:
        writer.writerow([
            save.date, 
            save.main_category.name if save.main_category else '',
            save.sub_category.name if save.sub_category else '',
            save.amount, 
            save.description
        ])

    return response

# ユーザー情報を表示する関数
def user_info(request):
    try:
        # ユーザーに紐付いたUserInfoデータを取得
        user_info = UserInfo.objects.get(user=request.user)
    except UserInfo.DoesNotExist:
        user_info = None  # UserInfoが存在しない場合はNoneを設定
    
    return render(request, 'budget/user_info.html', {'user_info': user_info})

# ユーザー情報を更新・保存する関数
def submit_user_info(request):
    try:
        # 既存のユーザー情報を取得
        user_info = UserInfo.objects.get(user=request.user)
    except UserInfo.DoesNotExist:
        # 存在しない場合は新規作成
        user_info = None

    if request.method == 'POST':
        # フォームをPOSTリクエストから取得
        form = UserInfoForm(request.POST, instance=user_info)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = request.user  # 現在のユーザーに紐付け
            user_info.save()
            return redirect('user_info')  # 保存後にユーザー情報ページへリダイレクト
    else:
        # フォームを空または既存のユーザー情報で表示
        form = UserInfoForm(instance=user_info)
    
    return render(request, 'budget/submit_user_info.html', {'form': form})

# ユーザーが保存した情報を表示する関数
def user_storage(request):
    try:
        # 現在のユーザーに関連するUserInfoデータを取得
        user_info = UserInfo.objects.get(user=request.user)
    except UserInfo.DoesNotExist:
        # UserInfoが存在しない場合、新規登録ページにリダイレクト
        return redirect('submit_user_info')

    return render(request, 'budget/user_storage.html', {'user_info': user_info})

