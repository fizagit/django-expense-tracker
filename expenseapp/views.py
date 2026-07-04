from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Budget
from .models import Expense
from django.shortcuts import get_object_or_404
import json
def home(request):
    return render(request, 'home.html')
def register_view(request):
    return render(request, 'register.html')
def login_view(request):
    return render(request, 'login.html')
def registration_view(request):
    if request.method == 'POST':
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"] 
        confirm_password=request.POST["confirm_password"]
        if password!= confirm_password:
            return render(request,'register.html')
        if User.objects.filter(username=username).exists():
            return render(request,'register.html')
        if User.objects.filter(email=email).exists():
            return render(request,'register.html')
       
        user=User.objects.create_user(username=username,email=email,password=password)
        return redirect('login')
    return render(request,'register.html')


#for authenticating login details got from registation pge and hence providing with the dashboard.

def login_user(request):
    if request.method == 'POST':

        username = request.POST.get('username') #if i wrote user_name instead of username inside get() ie, (mistook wrong var name wrote on login page, .get() returns a None instead of crashing the entire page,thats it)
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'login.html')

    return render(request, 'login.html')
        #Create your views here.



def logout_user(request):
    logout(request)
    return render(request,'home.html')

@login_required
def dashboard_view(request):

    budget = Budget.objects.filter(user=request.user).first()

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')
    
    budget_amount = budget.amount if budget else 0
   
    total_spent = sum(
        expense.amount
        for expense in expenses
    )
    remaining = budget_amount - total_spent
    notification = None
    notification_type = None
    
    category_totals = {}
    for expense in expenses:

        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount
    top_category = None
    top_amount = 0

    for category, amount in category_totals.items():

        if amount > top_amount:
            top_amount = amount
            top_category = category
    notification = None
    notification_type = None   
    if budget_amount > 0:

        usage_percentage = (total_spent / budget_amount) * 100

        if usage_percentage >= 80 and usage_percentage <= 100:
            notification = "⚠ You have used more than 80% of your budget."
            notification_type = "warning"

        elif usage_percentage > 100:
            notification = (
                    f"🚨 Budget exceeded.\n"
                    f"Highest spending category: {top_category} (₹{top_amount}).\n"
                    f"Consider reducing {top_category} expenses."
                )
            notification_type = "danger"
    chart_labels = list(category_totals.keys())
    chart_values = list(category_totals.values())


    category_totals_json = json.dumps(category_totals)
    return render(
        request,
        'dashboard.html',
        {
            'budget_amount': budget_amount,
            'expenses': expenses,
            'total_spent': total_spent,
            'remaining': remaining,
            "notification": notification,
            "notification_type": notification_type,
            "category_totals": category_totals, 
            'category_totals_json': category_totals_json  # IMPORTANT for chart

        }
    )

@login_required
def set_budget(request):

    budget, created = Budget.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        amount = request.POST.get("amount")

        budget.amount = amount
        budget.save()

        return redirect("dashboard")

    return render(
        request,
        "budget.html"
    )

@login_required
def add_expense(request):

    if request.method == "POST":

        Expense.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            amount=request.POST.get("amount"),
            category=request.POST.get("category"),
            date=request.POST.get("date")
        )

        return redirect('expenses')

    return render(request,"add_expense.html")

@login_required
def delete_expense(request, expense_id):

    if request.method == "POST":

        expense = get_object_or_404(
            Expense,
            id=expense_id,
            user=request.user
        )

        expense.delete()

    return redirect('expenses')

@login_required
def expenses_view(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'expenses.html',
        {
            'expenses': expenses
        }
    )
@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.category = request.POST.get("category")
        expense.date = request.POST.get("date")

        expense.save()

        return redirect('expenses')

    return render(
        request,
        'edit_expense.html',
        {
            'expense': expense
        }
    )

