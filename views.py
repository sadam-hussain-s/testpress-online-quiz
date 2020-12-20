#import modules according to the need
from django.shortcuts import render
from .models import Questions, ScienceQuestions, User
from django.core.paginator import Paginator


username =[] #to store username
lst =[] #to store user answers
anslist = [] #to store correct answers

#to retrive table data by variables
answers = Questions.objects.all() 
ScienceQuestionsanswers = ScienceQuestions.objects.all()

#for loop to store correct answer in list 
for i in answers:
    anslist.append(i.answer)
for j in ScienceQuestionsanswers:
    anslist.append(j.answer)


def home(request):
    return render(request, 'home.html')


def welcome(request):
    username.clear() #clear list to store new user
    uname = request.POST.get('username')
    username.append(uname)
    lst.clear() #clear list to store new user answers
    return render(request, 'welcome.html', {'username':username[0]})


def ScienceQuiz(request): #this method is for second quiz
    obj1 = ScienceQuestions.objects.all() #to retrive data from database
    paginator = Paginator(obj1,1) #using paginator to show each question in each page
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        sciencequestions = paginator.page(page)
    except(EmptyPage,InvalidPage):
        sciencequestions = paginator.page(paginator.num_pages)

    return render(request, 'ScienceQuiz.html', {'obj1':obj1, 'sciencequestions':sciencequestions})


def quiz(request): #this method is for first quiz
    obj = Questions.objects.all()
    paginator = Paginator(obj,1)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        questions = paginator.page(page)
    except(EmptyPage,InvalidPage):
        questions = paginator.page(paginator.num_pages)

    return render(request, 'quiz.html', {'obj':obj, 'questions':questions})

def result(request):
    score = 0
    for i in range(len(lst)): #for loop to check answers
        if len(lst)==len(anslist): #if condition to check length of the both lists
            if lst[i]==anslist[i]: #if condition to check the answer
                score +=1
        else:
            warn = "SOME ERROR OCCURS, please refresh the page and try again or close the window and open it again !!!!"
            return render(request, 'home.html', {'warn':warn}) #return home page with error message
    SaveData = User(StudentName=username[0], Scores=score) #to store data to database
    SaveData.save()
    return render(request, 'result.html', {'score':score, 'username':username[0]})


def saveans(request):
    ans = request.GET['ans'] #get the user answer without refreshing the page
    lst.append(ans) #append the user answer to list

