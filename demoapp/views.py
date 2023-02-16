import json
import traceback
# from tkinter.messagebox import QUESTION 
from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests import Response, session
from demoapp.models import Examportal,Questions, Score


from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

# @api_view(['GET'])
# def getallusers2(request):
#     usersfromdb=Userdata.objects.all()
#     print(usersfromdb)
#     serilizer=UserdataSerializer(usersfromdb,many=True)
#     return Response(serilizer.data)

def homepage(request):
    return render(request,'login.html')

def showregister(request):
    return render(request,'register.html')

def checkUsername(request):
    print(request.GET["name"])
    message="username already present"
    try:
        userdata=Examportal.objects.get(name=request.GET["name"])
        print(userdata)
    except:
        message='username does not exist'

    data={
        'message':message
       
        }
    json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
    print(json_data)
    response=HttpResponse(f'{json_data}',content_type='application/json')
    return response

def savedata(request):
    name=request.GET['name']
    password=request.GET['password']
    mobno=request.GET['mobno']
    email=request.GET['email']
    Examportal.objects.create(name=name,password=password,mobno=mobno,email=email)
    return render(request,'login.html',{'message':'Registration successfull,please login'})

def register(request):
    name=request.GET['name']
    password=request.GET['password']
    mobno=request.GET['mobno']
    email=request.GET['email']
    
    try:
        Examportal.objects.create(name=name,password=password,mobno=mobno)
    except:
        return render(request,'register.html',{'message':'user already present',"name":name,"password":password,"mobno":mobno,"email":email})
    return render(request,'login.html',{'message':'Registration sucessfull.'})

 
def login(request):
    #for admin user
    uname=request.GET['uname']   # username coming from browser uname=jbk
    upass=request.GET['upass']    # password coming from browser upass=python
    subject=request.GET['subject']

    if uname=="admin" and upass=="admin123":
       return render(request,'qmanag.html',{'message':"welcome admin"})
   
    try:
      usersfromdb=Examportal.objects.get(name=uname)#users.objects.get(username='jbk')
      print(usersfromdb) # usersfromdb is object of Userdata class .
    except:
      return render(request,'login.html',{'res':'wrong Username or password'})

    
    #it is having data from database 
    if uname==usersfromdb.name and upass==usersfromdb.password:
        questions=Questions.objects.filter(subject=subject)
        question=questions[0]
        request.session['qno']=0
        request.session['name']=uname
        request.session['subject']=subject
        
        request.session['answer']={}
        request.session['score']=0
        
        
        return render(request,'welcome.html',{'question':question})	    
    else:
        return render(request,'login.html',{'res':'wrong credential'})

#  session
def next(request):
    subject=request.GET['subject']
    
    questions=Questions.objects.filter(subject=subject)
    if(request.session['qno']<len(questions)-1):
        request.session['qno']=request.session['qno']+1
        question=questions[request.session['qno']]
        qno=question.qno
        response=request.session['answer'] # get dictionary
        previous=""
        for key,value in response.items():
            if(int(key)==qno):
                previous=value[3]
                break
    else:
        responses2=request.session['answer'] # get dictionary

        lastQuestion=questions[len(questions)-1]
        fqno=lastQuestion.qno
        preans=""
                
        # in operator is used to check presence of key in dictionary

        if(str(fqno) in responses2):
            lastanswer=responses2[str(fqno)]
            preans=lastanswer[3]
        else:
            preans=""
        return render(request,'welcome.html',{'errormessage':'Questions are over',"question":questions[len(questions)-1],'previous':preans})
    return render(request,'welcome.html',{'question':question,"previous":previous,"Totalquestions":len(questions),"Attemptedquestions":len(request.session['answer']),"Remainingquestions":len(questions)-len(request.session['answer'])})	

def previous(request):
    subject=request.GET['subject']
    questions=Questions.objects.filter(subject=subject)
    if(request.session['qno']>0):
        request.session['qno']=request.session['qno']-1
        question=questions[request.session['qno']]
        qno=question.qno
        response=request.session['answer'] # get dictionary
        previous=""
        for key,value in response.items():
            if(int(key)==qno):
                previous=value[3]
                break
    else:
        return render(request,'welcome.html',{"errormessage":'This is starting question',"question":questions[0]})
    
    return render(request,'welcome.html',{'question':question,"previous":previous})	
    
def result(request):
    return render(request,'score.html')

def endpage(request):
    del request.session['name']
    #print("username from session is ",request.session['username'])
    return render(request,"endpage.html")

def storeans(request):
    print("values are :",request.GET["qno"],request.GET["qtext"],request.GET["qanswer"],request.GET["op"])
    
    ans=request.session['answer'] # get dictionary
    
    ans[request.GET['qno']]=list([request.GET['qno'],request.GET['qtext'],request.GET['qanswer'],request.GET['op']])# update dictionary
    
    request.session['answer']=ans  # update answer attribute
    print(ans)
    return render(request,'welcome.html')
    
def answerschecking(request):
    try:
        responses=request.session['answer']
        allanswers=responses.values()
        for answer in allanswers:
             if(answer[2]==answer[3]):
                request.session['score']=request.session['score']+1
        del request.session['answer']
    except:
           traceback.print_exc()
           return render(request,'login.html')
    # print("all answers =",allanswers)
    # print("Final score is =",request.session['score'])
     
    #store score in database 
    name=request.session['name']
    subject=request.session['subject']
    score=request.session['score']
    try:
        Score.objects.create(name=name,subject=subject,score=score)
    except:
        return render(request,'login.html',{'msg':"Try with another subject"})
        
    return render(request,'score.html',{'allanswers':allanswers,'finalscore':request.session['score']})


def viewQuestion(request):
        print(request.GET['qno'])
        print(request.GET['subject'])
        question=Questions.objects.get(qno=request.GET['qno'],subject=request.GET['subject'])
        print(question)
        data={ 
        'qtext':question.qtext,
        'qanswer':question.qanswer,
        'op1':question.op1,
        'op2':question.op2
        }
        json_data=json.dumps(data) # dumps() converts python dictionary into JSON String
        print(json_data)
        response=HttpResponse(f'{json_data}',content_type='application/json')
    
        return response
    
    
def saveQuestions(request):
    qno=request.GET['qno']
    qtext=request.GET['qtext']
    qanswer=request.GET['qanswer']
    op1=request.GET['op1']
    op2=request.GET['op2']
    subject=request.GET['subject']
    Questions.objects.create(qno=qno,qtext=qtext,qanswer=qanswer,op1=op1,op2=op2,subject=subject)
    print("question added to the database")
    return render(request,"qmanag.html",{"message":"Question is added"})
    
def updateQuestion(request):
    que=Questions.objects.filter(qno=request.GET['qno'],subject=request.GET['subject'])
    
    que.update(qtext=request.GET['qtext'],qanswer=request.GET['qanswer'],op1=request.GET['op1'],op2=request.GET['op2'])
    
    return render(request,"qmanag.html",{"message":"Question is updated"})

def deleteQuestion(request):
    Questions.objects.filter(qno=request.GET['qno'],subject=request.GET['subject']).delete()
    return render(request,"qmanag.html",{"message":"Question is deleted"})


def adminpage(request):
    return render(request,"admin.html")