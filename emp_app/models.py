from django.db import models
from django.contrib.auth.models import User

class Shop_Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField() 
    phone = models.CharField(max_length=10)  
    address = models.CharField(max_length=100, default=None)    

    def __str__(self):
        return self.name

class Shop_Admin(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
   name=models.CharField(max_length=15)
   password=models.CharField(max_length=100)  
   def __str__(self):
      return self.name

class Shop_Sale(models.Model):
   employee=models.ForeignKey(Shop_Employee,on_delete=models.CASCADE,null=True,blank=True)
   Amount=models.IntegerField()
   Type=models.CharField(max_length=25)
   # Time=models.DateTimeField(auto_now_add=True)
   date = models.DateField(auto_now_add=True)
   time = models.TimeField(auto_now_add=True)
   def __str__(self):
      return self.employee.name


class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Shop_Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    def __str__(self):
      return self.employee.name

