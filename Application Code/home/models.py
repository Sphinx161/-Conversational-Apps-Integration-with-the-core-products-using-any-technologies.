# Create your models here.
from django.db import models

# Create your models here.
class Managers(models.Model):
    MId = models.TextField()
    userName = models.CharField(max_length=100)
    password = models.TextField()
    compName = models.CharField(max_length=50)
    secretPswd = models.TextField()
    emailid = models.EmailField(max_length=254)

    def __str__(self):
        return self.userName + '-' + self.MId

class Employees(models.Model):
    MId = models.TextField()
    EId = models.TextField()
    EmpName = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    dob = models.CharField(max_length=10)
    doj = models.CharField(max_length=10)
    salary = models.IntegerField()
    desgn = models.TextField()
    bname = models.CharField(max_length=40)
    hcity = models.CharField(max_length=30)
    mobile = models.IntegerField()
    leaveTaken = models.IntegerField()

# a = Employee(MId="B218050", EId="52164", EmpName=
# "Ansuya", gender="F", email="ansuyamohapatra03@gmail.com", dob="2000-10-5", age="19", doj=12, salary="25000", desgn="intern", bname="bbsr", hcity="bbsr", mobile="9874736478", pswd="ansuya04", leaveTaken="two", aic="one")


