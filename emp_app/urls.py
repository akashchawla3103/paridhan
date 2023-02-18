from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin_login',admin_login,name='admin_login'),
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('register_employee',register_employee,name='register_employee'),
    path('handle_logout',handle_logout,name='handle_logout'),
    path('Sale',Sale,name='Sale'),
    path('view_sales',view_sales,name='view_sales'),
    path('view_commission',view_commission,name='view_commission'),
    path('update_c',update_c,name='update_c'),
    path('home', home, name='home'),
    path('delete_sales/<id>',delete_sales,name='delete_sales'),
    path('update_sales/<id>',update_sales,name='update_sales'),
    path('sale_update_action',sale_update_action,name='sale_update_action'),
    path('delete_employee',delete_employee,name='delete_employee'),
    path('delete_employee_action/<id>',delete_employee_action,name='delete_employee_action'),
    path('attendance_employee',attendance_employee,name='attendance_employee'),
    path('mark_attendance/<id>',mark_attendance,name='mark_attendance'),
    






]
# static files
urlpatterns+=staticfiles_urlpatterns()