from django.urls import path
from . import views
urlpatterns = [ path('',views.home,name='home'),
                path('register/',views.register_view,name='register'),
                path('login/',views.login_view,name='login'),
                path('registration/',views.registration_view,name='registration'),
                path('login-user/', views.login_user,name='login_user'),#login-user is just path created there itself, i can add wtvr name there
                path('dashboard/', views.dashboard_view,name='dashboard' ),#refer views.py in the login_user fucntion return dashboard 
                path('logout-user/',views.logout_user,name='logout_user'),
                path('budget/',views.set_budget,name='set_budget'),
                path('add-expense/',views.add_expense, name='add_expense'),
                path('delete-expense/<int:expense_id>/',views.delete_expense,name='delete_expense'),
                path('expenses/',views.expenses_view,name='expenses'),
                path('edit-expense/<int:expense_id>/',views.edit_expense,name='edit_expense'),
               ]
 