# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 11:41:21 2020

@author: CVNAD
"""

# importing packages
from word2number import w2n
import spacy
import re
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def main_function(text):
    bot  = ChatBot('Kookie',
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
    
    for files in os.listdir('./english/'):
        data=open('./english/'+files,'r').readlines()
        trainer.train(data)
    
    nlp = spacy.load('en')
    
    # keywords
    keywords = {'email':[1],'send':[1,2],'open':[3],'search':[6],'kookie':[7],'details':[2]}
    
    actions = {1:'redirecting to mail',2:'fetching details',3:'opening the required webpage',6:'searching in browser',7:"hello! how can i help you with?"}
    
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
            if(i[1] in ['NN','NNP','VB','JJ','NNS','VBP']):
                if(i[0] in keywords.keys()):
                    action_keywords.append(i[0])
                else:
                    database_keywords.append(['s',i[0]])
        return [action_keywords,database_keywords]
    
    def email_id(text):
        text = re.sub(' at the rate ','@',text)
        text = re.sub(' dot ','.',text)
        text = text.split()
        text = ''.join(text)
        return text
    
    # testing section
    text = text.lower()
    if(text == 'stop'):
        print("")     # direct a call to stop the chatbot
    else:
        reply = bot.get_response(text)
        reply = str(reply)
    # reply = input()
        if(reply == 'algo'):
        # text = input()
            text = date_time(text)
            [action_keywords,database_keywords] = listing(text)
            act = action(action_keywords)[0]
            if(act == 1):
                print('please specify the email id') # speak this
                email_text = input()
                email_text = email_id(email_text)
                database_keywords.append(email_text)
            if(act == 2):
                print('please specify name') # speak this
                details_text = input()
                database_keywords.append(details_text)
                print('Kookie:',actions[act])
        else:
            print('Kookie:',reply)
text = input()
main_function(text)
    