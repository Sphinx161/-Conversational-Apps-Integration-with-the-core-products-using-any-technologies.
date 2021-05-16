from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from word2number import w2n
import spacy
import re
import os
import webbrowser
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
from bs4 import BeautifulSoup
from home.models import Managers,Employees
import smtplib
from .models import Store
from . import search

my_list=[]

def main_function(text):
    bot  = ChatBot('kookie',
        #storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'algo',
                #'maximum_similarity_threshold': 0.90
            },
    #        {
    #            'import_path': 'chatterbot.logic.TimeLogicAdapter',
                #'maximum_similarity_threshold': 0.90
    #        },
    #        {
    #            'import_path': 'chatterbot.logic.MathematicalEvaluation',
                #'maximum_similarity_threshold': 0.90
    #        },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'help me',
                'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org' 
            }
        ]       
    )
    
    trainer = ListTrainer(bot)
    
    trainer.train([
    "good morning",
    "Hello there!"
    "hello cookie",
    "Hello! What's it that you need?",
    "goodbye",
    "Okay meet you soon!",
    "i like you",
    "I like you too.",
])
    
    nlp = spacy.load('en')
    
    # keywords
    keywords = {'message':[1],'email':[1],'send':[1,2],'open':[3],'search':[6],'cookie':[7],'details':[2]}
    
    actions = {1:'Please tell me your message',2:'fetching details',3:'opening the required webpage',6:'searching in browser',7:"hello! how can i help you with?"}
    
    # dictionary mapping words to characters
    dictionary = {'first':'1','second':'2','third':'3','fourth':'4','fifth':'5','sixth':'6',
                  'seventh':'7','eighth':'8','ninth':'9','tenth':'10','eleventh':'11',
                  'twelfth':'12','thiteenth' : '13','fourteenth':'14','fifteenth':'15',
                  'sixteenth':'16','seventeenth':'17','eighteenth':'18','nineteenth':'19'}
    
    # months dictionary
    month_dict = {'jan':'01','january':'01','feb':'02','february':'02','mar':'03','march':'03',
                  'april':'04','may':'05','june':'06','july':'07',
                  'aug':'08','august':'08','sep':'09','september':'09',
                  'oct':'10','october':'10','november':'11','december':'12'}
    # action function
    def action(l):
        a=[]
        if(l == []):
            return [6]
        for i in l:
            for j in keywords[i]:
                if j not in a:
                    a.append(j)
                else:
                    a = [j]
        return a
    
    # function for date
    def date_time(text):
        text = re.sub(' at the rate ',' @ ',text)
        text = re.sub(' dot ',' . ',text)
        l = text.split()
        l.append('garbage value')
        p = []
        i=0
        while(i<len(l)-1):
            if(l[i] in dictionary):
                p.append(dictionary[l[i]])
                i=i+1
            elif(w2n.word_to_num(l[i])==0):
                p.append('0')
                i=i+1
            elif(not(w2n.word_to_num(l[i])=='' or w2n.word_to_num(l[i])==0)):
                s = '' + str(l[i])
                i=i+1
                while(not(w2n.word_to_num(l[i])=='')):
                    s = s+' '+ str(l[i])
                    i=i+1
                p.append(str(w2n.word_to_num(s)))
            else:
                p.append(l[i])
                i=i+1
        p.append('garbage_value')
        f=[]
        i = 0
        while(i<len(p)-1):
            if(str(p[i]).isdigit() and str(p[i+1]).isdigit()):
                f.append(str(p[i]+p[i+1]))
                i = i+2
            elif(p[i] in month_dict):
                f.append(month_dict[p[i]])
                i = i+1
            else:
                f.append(p[i])
                i = i+1
        
        t = ' '.join(f)
        t = re.sub(' @ ','@',t)
        t = re.sub(' \. ','.',t)
        t = re.sub('email id','emailid',t)
        f = t.split()
        f.append('garbage_value')
        i = 0
        j = []
        while(i<len(f)-1):
            if(f[i] == 'emailid'):
                i= i+1
                s = '' + f[i]
                i=i+1
                while(not('@' in f[i]) and i < len(f)-1):
                        s = s + f[i]
                        i = i+1
                s = s + f[i]
                i = i+1
                j.append(s)
            else:
                j.append(f[i])    
                i = i+1
        t = ' '.join(j)
        return t
    
    # list of keywords function
    def listing(text):
        o = nlp(text)
        k = [(word.text,word.tag_) for word in o]
        action_keywords = []
        database_keywords = []
        m1 = re.findall('\d{1,2}-\d{1,2}-\d{4}',text)
        m2 = re.findall('\d{1,2}/\d{1,2}/\d{4}',text)
        m3 = re.findall('(\d{1,2} \d{1,2} [a|p]m)+',text)
        m4 = []
        for i in m1:
            database_keywords.append(['date',i])
        for i in m2:
            database_keywords.append(['date',i])
        for i in m3:
            database_keywords.append(['time',i])
        for i in m4:
            database_keywords.append(['email_id',i])
        for i in k:
            if(i[1] in ['NN','NNP','VB','JJ','NNS','VBP','VBG']):
                if(i[0] in keywords.keys()):
                    action_keywords.append(i[0])
                else:
                    database_keywords.append(i[0])
        my_list = database_keywords
        return [action_keywords,database_keywords]
    
    # list of email_id to send the mail
    def send_mail(email_id, message):
        # li = [email_id] 
        # for dest in li:
        print("173-Reached send mail" + email_id) 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("dummy.org.123@gmail.com", "dummy@123") 
        s.sendmail("dummy.org.123@gmail.com", email_id, message) 
        s.quit()
    
    # testing section
    text = text.lower()
      # direct a call to stop the chatbot

    #reply = bot.get_response(text)
    #reply = str(reply)
    #if(reply == 'algo'):
        #text = date_time(text)
    [action_keywords,database_keywords] = listing(text)
    act = action(action_keywords)[0]
    if(act == 1):
        if('my message is' in text):
            p = text
            p = re.sub('my message is','mymessageis',p)
            p = p.split()
            i=0
            p.append('garbage_value')
            while(i<len(p)-1):
                if(p[i]=='mymessageis'):
                    i = i+1
                    s = []
                    while(i<len(p)-1):
                        s.append(p[i])
                        i=i+1
                i=i+1
            s = ' '.join(s)
            em=''
            st = Store.objects.all()
            for item in st:
                em = item.sendEmail
            send_mail(em,s)
            return ('message sent')
        q = text
        print("194 - this is the text" + q)
        q = q.lower()
        q = re.sub('email id','emailid',q)
        q = re.sub(' at the rate ','@',q)
        q = re.sub(' @ ','@',q)
        q = re.sub(' dot ','.',q)
        q = re.sub(' \. ','.',q)
        q = q.split()
        q.append('garbage_value')
        i = 0
        s = '' 
        while(i<len(q)-1):
            if(q[i]=='emailid'):
                i = i+1
                while(i<len(q)-1):
                    s = s + q[i]
                    i = i+1
            i = i+1
        print("its the final mailid" + s)
        st = Store.objects.create(sendEmail=s)
        st.save() 
            
    if(act == 2):
        result = fetchDataBase(database_keywords)
        return result
    if(act==3):
        text = text.split()
        search.searchWebPage(text[1])
        print("text[1]"+text[1])
        return actions[act]
    if(act==6):
        if('search' not in text):
            searchInBrowser(text)
            return actions[act]
        text = text.lower()
        text = text.split()
        text.append('garbage_value')
        s = ''
        i=0
        while(i<len(text)-1):
            if(text[i] == 'search'):
                i=i+1
                while(i<len(text)-1):
                    s = s+text[i]
                    i=i+1
            i=i+1
        print("What are we searching "+s)
        searchInBrowser(s)
        return actions[act]

    result = actions[act]
    print('Kookie:',actions[act])
    #else:
        #result = reply
    return result
      
    
# from json import dumps
# Create your views here.
def chat(request):
    # if(request.GET.get('msg')):
    if request.is_ajax():
       print("hi you came to chat page!")
       print("1st line python file method...")
       # print(request.GET.get('msg'))
       txt = request.GET.get('msg')
       print("Msg in chat function :"+txt)
       result = main_function(txt)
       return JsonResponse({'ReturnAnswer':result},status=200)
    else:
      return render(request,"chat.html")


# main_function(text)   

def searchInBrowser(txt):
   webbrowser.open('https://www.google.com/?#q=' + txt)


def fetchDataBase(my_list):
    emp = Employees.objects.all() 
    l = []
    ename=''
    for i in my_list:
        i=i.lower()
        print("i :"+i)
    for item in emp:
        item.EmpName = item.EmpName.lower()
        print(item.EmpName)
        l.append(item.EmpName)
        
    for name in l:
        for data in my_list:
            if(data == name):
                print("data == name ::"+name)
                ename = name    
    for e in emp:
        print("e in emp :"+e.EmpName+" ename :"+ename)
        e.EmpName=e.EmpName.lower()
        if e.EmpName == ename:
            print("Equal names ! ")
            for item in my_list:
                if item in ['contact','mobile','phone']:
                    print("equal names : 1")
                    return 'Mobile number of '+ename+'::'+str(e.mobile)
                elif item in ['email','mail','emailid']:
                    print("equal names : 2")
                    return 'Email ID of '+ename+'::'+str(e.email)
                elif item in ['salary','income','wage','payroll']:
                    print("equal names : 3")
                    return 'Salary of '+ename+'::'+str(e.salary)
                elif item in ['leaves','leave']:
                    print("equal names : 4")
                    return 'Leaves Taken of '+ename+'::'+str(e.leaveTaken)
                elif item in ['date of birth','birthday','birth','birthdate','age','dob']:
                    print("equal names : 5")
                    return 'DOB of'+ename+'::'+str(e.dob)
                elif item in ['join','joining','experience','date of joining']:
                    print("equal names : 6")
                    return 'DOJ of '+ename+'::'+str(e.doj)
    return "Sorry didn't get anything in the database! :)"
        