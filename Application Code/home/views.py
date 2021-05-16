from django.shortcuts import render,redirect
from . models import Managers
def home(request):
    return render(request,"index.html")

def signin(request):
   if request.method == 'POST':
       manager = Managers.objects.all()
       givenEmail = request.POST['email']
       passwd = request.POST['password']
       print("Given email:"+givenEmail)
       print("Given password :"+passwd)
       i = 0
       for m in manager:
          print("Email DB :"+m.emailid)
          print("Password DB :" + m.password)
          print("Mid DB :" + m.MId)
          if(givenEmail==m.emailid and passwd==m.password):
              print("I m inside homepage yahoooooooooooooooooooooo")
              return render(request,"chat.html",{'name' :m.userName,'emailid': m.emailid,'Mid': m.MId})
              i=1
       if i==0:
           return render(request,"index.html")
   else:
       return render(request,"index.html")

def signup(request):
    print("I am in signup function()....")
    if request.method == 'POST':
        mid = request.POST['createMid']
        username = request.POST['createUserName']
        password = request.POST['createPassword']
        cname = request.POST['createCompanyName']
        spass = request.POST['secret']
        memail = request.POST['createEmail']
        print(mid+" "+username+" "+password+" "+cname+" "+spass+" "+memail)
        manage = Managers.objects.create(MId=mid,userName=username,password=password,compName=cname,secretPswd=spass,emailid=memail)
        manage.save()
        return render(request,"index.html")
    else:
        return render(request,"index.html")