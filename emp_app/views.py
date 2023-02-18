import calendar
from django.core import serializers
from django.http import JsonResponse
from .models import *
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.db.models import Sum
from datetime import date,time, timedelta, timezone
from django.db.models import Q
from django.utils import timezone
import datetime

# Create your views here.

def home(request):
    employees = Shop_Employee.objects.all()
    return render(request, 'home.html', {'employees': employees})

@login_required(login_url='/admin_login')
def Sale(request):
    # get the present employees
    present_members = EmployeeAttendance.objects.filter(status='Present', date=date.today()).values_list('employee', flat=True)
    # present_members = EmployeeAttendance.objects.filter(status='Present', date=date.today())
    # print(present_members)    
    employees = Shop_Employee.objects.filter(id__in=present_members)
    
    if request.method == 'POST':
        s_id = request.POST.get("id")
        s_Amount = int(request.POST.get("Amount"))
        s_Type = request.POST.get("Type")
        s_employee = employees.get(name=s_id)
        sale_details = Shop_Sale(employee=s_employee, Amount=s_Amount, Type=s_Type)
        sale_details.save()
        messages.success(request, "Saved Successfully")
    
    context = {'Employees': employees}
    return render(request, 'sale.html', context)


def admin_dashboard(request):
    employees={"1":"Sandeep","2":"Sameer","3":"Bharkya","4":"Rohit"}
    return render(request,'admin_dashboard.html',employees)

@login_required(login_url='/admin_login')
def register_employee(request):
   if request.method=='POST':
        e_email=request.POST.get("email")
        e_name=request.POST.get("name")
        e_mobile=request.POST.get("mobile")
        e_add=request.POST.get("address")
        print(str(e_mobile))
        print(e_email)
        employee_details=Shop_Employee(name=e_name,email=e_email,phone=e_mobile,address=e_add)
        employee_details.save()
        messages.success(request,"Saved Sucessfully")
   return render(request,'register_employee.html')

def admin_login(request):
    if request.method=='POST':
        a_name=request.POST.get("name")
        a_password=request.POST.get("password")
        user=User.objects.filter(username=a_name).first() 
        print(a_name)
        print(a_password)
        print(user)
        if user is None:
            messages.success(request,"User not found")
            return redirect('/admin_login')

        user_auth=authenticate(username=user,password=a_password)
        if user_auth :
            login(request,user)
            # messages.success(request,user.username)
            return redirect('/register_employee')
        else:
            messages.success(request,"You have entered a wrong Password")
            return redirect('/admin_login')


    return render(request,"admin_login.html")      

    
def handle_logout(request):
    # if request.method=='POST':
        logout(request)
        messages.success(request,"You are Logged Out")
        return redirect('/admin_login')

def view_sales(request):
    sales=Shop_Sale.objects.all()
    context={'sales':sales}
    return render(request,"view_sales.html",context)

def delete_sales(request,id):
    try:    
        detail=Shop_Sale.objects.get(id=id)
        detail.delete()
    except Shop_Sale.DoesNotExist:
        pass
    return  redirect('view_sales')

def update_sales(request,id):
    try:    
        detail=Shop_Sale.objects.get(id=id)
        request.session['update_id'] = id
        update_status=True
        Employees=Shop_Employee.objects.all()

        context={'detail':detail,'Employees':Employees}
        return render(request,'update_sales.html',context)
    except Shop_Sale.DoesNotExist:
        pass
    return  redirect('view_sales')

def sale_update_action(request):
    if request.method=='POST':
        print(request.session['update_id'])

        id1=request.session['update_id'] 
        print(id1)
        sale_update=Shop_Sale.objects.get(id=id1)
        print(sale_update)

     
        s_id=request.POST.get("id")
        s_employee=Shop_Employee.objects.all().get(name=s_id)

        s_Amount=int(request.POST.get("Amount"))
        s_Type=request.POST.get("Type")

        sale_update.employee=s_employee    
        sale_update.Amount=s_Amount
        sale_update.Type=s_Type
        # d= date(2023, 2, 10)
        # sale_update.date=d.strftime('%Y-%m-%d')
        sale_update.save()
        redirect('view_sales')
    
    return redirect('view_sales')

def view_commission(request):
    s_date = None
    s_date = datetime.datetime.now().date() 
    employees = Shop_Employee.objects.all()
    total_sales=None
    employee_commission = []
    for employee in employees:
        total_sales = Shop_Sale.objects.filter(employee=employee,date__month=s_date.month,date__year=s_date.year,time = time(13,19,0)).aggregate(total_sales=Sum('Amount'))
        if total_sales['total_sales']:
            commission = (total_sales['total_sales']) * 0.01
            employee_commission.append({'employee': employee, 'totalsales':total_sales  ,'commission': commission})
            return JsonResponse({"com":employee_commission})
    return render(request, 'view_commission.html', {'employee_commission': employee_commission})

def update_c(request):
    selected_date = request.GET.get('selection')
    employee_commission = []
    employees = Shop_Employee.objects.all()
    
    if selected_date == 'today':
        sale_date = date.today()
        for employee in employees:
            total_sales = Shop_Sale.objects.filter(employee=employee, date=sale_date).aggregate(total_sales=Sum('Amount'))
            if total_sales['total_sales']:
                commission = total_sales['total_sales'] * 0.01
                employee_commission.append({'employee_id': employee.id,'employee_name':employee.name, 'total_sales': total_sales['total_sales'], 'commission': commission})
            print(employee_commission)
        response_data = {'employee_commission': employee_commission}

    elif selected_date == 'month':
        sale_date = date.today().replace(day=1)
        till_sale_date=date.today()
        for employee in employees:
            total_sales = Shop_Sale.objects.filter(employee=employee, date__gte=sale_date,date__lte=till_sale_date).aggregate(total_sales=Sum('Amount'))
            if total_sales['total_sales']:
                commission = total_sales['total_sales'] * 0.01
                employee_commission.append({'employee_id': employee.id,'employee_name':employee.name, 'total_sales': total_sales['total_sales'], 'commission': commission})
            print(employee_commission)
        response_data = {'employee_commission': employee_commission}
    return JsonResponse(response_data)

    # else:
    #     sale_date = date.today()

   
    # for employee in employees:
    #     total_sales = Shop_Sale.objects.filter(employee=employee, date_=sale_date).aggregate(total_sales=Sum('Amount'))
    #     if total_sales['total_sales']:
    #         commission = total_sales['total_sales'] * 0.01
    #         employee_commission.append({'employee_id': employee.id, 'total_sales': total_sales['total_sales'], 'commission': commission})
    #     print(employee_commission)
    # response_data = {'employee_commission': employee_commission}
    
# def update_c(request):
#     s_date=0
#     if request.method == 'GET':
#         date=request.GET.get('selection')
#         print(date)
#         if date == 'today':
#             s_date = datetime.datetime.now().date()
#         elif date == 'month':  
#             now = datetime.datetime.now()
#             s_date = datetime.date(now.year, now.month, 1)

#     employees = Shop_Employee.objects.all()
#     employee_commission = []
#     for employee in employees:
#         total_sales = Shop_Sale.objects.filter(employee=employee,date__month=s_date.month,date__year=s_date.year,time = time(13,19,0)).aggregate(total_sales=Sum('Amount'))
#         if total_sales['total_sales']:
#             commission = (total_sales['total_sales']) * 0.01
#             employee_commission.append({'employee': employee, 'totalsales':total_sales  ,'commission': commission})
#     response_data = {
#         'employee_commission': employee_commission,
        
#     }
#     return JsonResponse(response_data)

@login_required
def delete_employee(request):
    employees = Shop_Employee.objects.all()
    
    context={'employees':employees}
    return render(request,'delete_employee.html',context)

@login_required
def delete_employee_action(request,id):
    try:    
        employee=Shop_Employee.objects.get(id=id)
        employee.delete()
    except Shop_Employee.DoesNotExist:
        pass
    return  redirect('delete_employee')

# def attendance_employee(request):
#     employees = Shop_Employee.objects.all()
#     attendances=EmployeeAttendance.objects.all()
    
#     present_members=attendances.filter(status="Present",date=date.today())
#     a_members=attendances.filter(status="Present",date=date.today())

#     print(present_members)
#     absent_members = Shop_Employee.objects.filter(~Q(id__in=attendances.values('employee_id')))
#     print(absent_members)
        
#     context={'employees':employees,'p_employees': present_members,'a_employees':absent_members,'calendar': calendar}
#     return render(request,'attendance.html',context)

# def mark_attendance(request,id):
#     a_employee=Shop_Employee.objects.get(id=id)
#     print(a_employee)
#     Attendance=EmployeeAttendance(employee=a_employee,status="Present")
#     Attendance.save()
#     return redirect('attendance_employee')
    


from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from .models import Shop_Employee, EmployeeAttendance
# from datetime import datetime, date, time


def attendance_employee(request):
    employees = Shop_Employee.objects.all()


    attendances = EmployeeAttendance.objects.all()
    print("Employees:")
    print(employees)
    # print("Attendance:"+""+attendances)
    today = date.today()  # get today's date and time
    tomorrow = today - timedelta(days=1)
    # present_members = attendances.filter(status="Present", date=today)
    # # absent_members = Shop_Employee.objects.filter(~Q(id__in=attendances.values('employee_id')))
    # absent_members = Shop_Employee.objects.filter(~Q(id__in=attendances.values('employee_id')))
    present_members = attendances.filter(status="Present", date=today)
    absent_members = Shop_Employee.objects.exclude(id__in=present_members.values('employee_id'))


    print(present_members)
    print(absent_members)
    context = {'employees': employees, 'p_employees': present_members, 'a_employees': absent_members}
    return render(request, 'attendance.html', context)


def mark_attendance(request, id):
    employee = get_object_or_404(Shop_Employee, id=id)

    attendance, created = EmployeeAttendance.objects.get_or_create(employee=employee, date=date.today())

    if created:
        attendance.status = "Present"
        # tomorrow = date.today() + timedelta(days=1)

        # attendance.date = tomorrow.strftime('%Y-%m-%d')
        attendance.save()
        messages.success(request, f"{attendance.employee} has marked attendance successfully!")
    else:
        messages.warning(request, f"{attendance.employee} has already marked attendance today.")

    return redirect('attendance_employee')

    