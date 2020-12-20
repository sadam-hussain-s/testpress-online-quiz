# testpress-online-quiz

Full source Code for Online Quiz :

Front end : HTML, CSS and Javascript
Back End : Django(python)
---------------------------------------------------------------------------------------------
------------------URLS OF ONLINE QUIZ APPLICATION--------------------

from django.contrib import admin
from django.urls import path
from quiz import views

#urls for the project
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    path('welcome/', views.welcome),
    path('quiz/', views.quiz),
    path('result/', views.result),
    path('saveans/', views.saveans),
    path('ScienceQuiz/', views.ScienceQuiz),
]

-------------------------------------------------------------------------------------------------------
----------------------VIEWS.PY FOR RENDERING PAGES------------------------------

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

----------------------------------------------------------------------------------------------------------------------

------------------------------------------------HOME PAGE CODE-------------------------------------------

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to the online Quiz</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    
</head>
<body>
    {{warn}}<!--show only when error occurs-->
    <div class="col-lg-8 border border-sucess p-4 m-4 mx-auto">

    <form class="form-to-get-username" action="/welcome/" method="POST">
        {% csrf_token %}
        <div>
            <div>
                <label for="username"><h2>Student Name</h2></label>
            </div>
            <div class="txt_field">
                <input type="text" name="username" id="uname" required class="form-control"/>
            </div>
            <br>
        </div>
        <button class="btn form-control btn-success" id="submit"><h2>Submit Name</h2></button>
    </form>
    </div>
</body>
</html>

--------------------------------------------------------------------------------------------------------------------

----------------------------WELCOME PAGE CODE TO START QUIZ-------------------------------

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to the online Quiz</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    
    <style>
        .title{
            color: aliceblue;
            background-color: blue;
            text-align: center;
        }
        .label{
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="col-lg-8 border border-sucess p-4 m-4 mx-auto">
        <h1 class="title">
            Online Quiz
        </h1>
        <form class="form-to-get-username">
            <br>
            <div class="label"><!--page to start the quiz-->
            <label><h2>Student Name : {{username}}</h2></label>
            </div>
            <br>
        </form>
        <a href="/quiz/"><button class="btn form-control btn-success" id="submit"><h2>Start Quiz</h2></button></a>

    </div>

</body>
</html>
-----------------------------------------------------------------------------------------------------------------------------
--FIRST SET QUIZ PAGE--

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    
    <script type="text/javascript">

    //prevent from roll back
    function preBack(){
        window.history.forward();
    }
    setTimeout("preBack()",0);
    window.onunload=function(){null};

    //code to create timer for each question
    var counter =15;
    setInterval( function(){
        counter--;

        if(counter>=0){
            id = document.getElementById("count");
            id.innerHTML =counter; //code to write in HTML
        }
        if(counter==0){
            id.innerHTML="Time Up";
            var hiddenDiv = document.getElementById("hidden");
            var DisabledButton = document.getElementById("submit");
            var HideOptions = document.getElementById("options");
                    
            hiddenDiv.style.display="block"; //display div
            DisabledButton.style.display="block"; //display hidden button
            HideOptions.style.display="none"; //hide options
            if(!checkForChecked){
                var ans = "wrong"; //if user not click any options, this is default value
                tosendData(ans); //function to send user answer
            }
        }
    }, 1000);

    let checkForChecked = false; //to check non checked option

    //function to send answer to views.py file
    function tosendData(data){
        var req=new XMLHttpRequest();
        var url = '/saveans?ans='+data;
        req.open("GET",url,true)
        req.send()
    }    

    //function to check the user click the radio button or not
    function func(){
        var type = document.getElementsByName("name");
        var hiddenDiv = document.getElementById("hidden");
        var DisabledButton = document.getElementById("submit");
        var HideOptions = document.getElementById("options");

        for(var i =0; i<type.length;i++){
            if(type[i].checked){
                var ans = type[i].value; //variable for user answer
                checkForChecked=true;
                hiddenDiv.style.display="block";
                DisabledButton.style.display="block";
                HideOptions.style.display="none"; 
            }
        }
        tosendData(ans);
    }
    </script>


    <style>
        #submit{
            display: none;
        }
        #hidden{
         display: none;  
         color: green;
        }
        section{
            display: flex;
            text-align: right;
            float: right;
            align-items: flex-start; 
        }
        span{
            text-align: center;
            color: red;
        }
        #id{
            background-color: blue;
            color: aliceblue;
            
        }
        .ques{
            width: auto;
            height: auto;
            background-color: blue;
            color: aliceblue;
        }
        
    </style>
</head>
<body>

<div class="col-lg-8 border border-sucess p-4 m-4 mx-auto">
    <section>
        <div class="container">
            <h3>Time Left : </h3><h3 id="count" style="border: 3px solid red;">15</h3>
        </div>
    </section>

    <!--Below code to inform user about the quiz-->
    <span><h3>*Once you click any option, it will hide the all options. So ANSWER CAREFULLY !!!</h3></span>
    {% for i in questions %} <!--code to retrive questions, options and answer by using for loop-->
    <br>
    <h1 class="ques">Set 1 - Question</h1><br> <div class="container1"><h2>{{i.question}}</h2></div><br><!--to get question-->
    <form>
        
    <div id="options">

        <div class="radio">
            <label><input type="radio" id="option1" name="name" value="{{i.option1}}" onclick="func()"><b> {{i.option1}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option2" name="name" value="{{i.option2}}" onclick="func()"><b> {{i.option2}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option3" name="name" value="{{i.option3}}" onclick="func()"><b> {{i.option3}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option4" name="name" value="{{i.option4}}" onclick="func()"><b> {{i.option4}}</b></label>
        </div>

    </div>
        <div id="hidden">
            <label><h2>Correct Answer is : {{i.answer}}</h2></label>
        </div>
        <br>
    </form>
    {% endfor %}<!--for loop end-->



    <div class="paginator"><!--paginator code-->
        <div class="form-group">
            {% if questions.has_next %}<!--if condition to check there is next page or not-->
                <a href="?page={{ questions.next_page_number}}"><button class="btn form-control btn-primary" id="submit">Next</button></a>
            {% else %}<!--below code change page to second quiz-->
                <a href="/ScienceQuiz/"><button class="btn form-control btn-primary" id="submit">Next Quiz</button></a>
            {% endif %}<!--end if-->
        </div>
    </div>
</div>


</body>
</html>

---------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------SECOND SET QUIZ PAGE--------------------------------------------------


<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Science Quiz Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    
    <script type="text/javascript">
    //prevent from roll back
    function preBack(){
        window.history.forward();
    }
    setTimeout("preBack()",0);
    window.onunload=function(){null};

    //code to create timer for each question
    var counter =15;
    setInterval( function(){
        counter--;
        if(counter>=0){
            id = document.getElementById("count");
            id.innerHTML =counter; //code to write in HTML
        }
        if(counter==0){
            id.innerHTML="Time Up";
            var hiddenDiv = document.getElementById("hidden"); 
            var DisabledButton = document.getElementById("submit");
            var HideOptions = document.getElementById("options");
            
            
            hiddenDiv.style.display="block"; //display div
            DisabledButton.style.display="block"; //display hidden button
            HideOptions.style.display="none"; //hide options
            if(!checkForChecked){
                var ans = "wrong"; //if user not click any options, this is default value
                tosendData(ans); //function to send user answer
            }   
        }
    }, 1000);

    let checkForChecked = false;

    //function to send answer to views.py file
    function tosendData(data){
        var req=new XMLHttpRequest();
        var url = '/saveans?ans='+data;
        req.open("GET",url,true)
        req.send()
    }    

    //function to check the user click the radio button or not
    function func(){
        var type = document.getElementsByName("name");
        var hiddenDiv = document.getElementById("hidden");
        var DisabledButton = document.getElementById("submit");
        var HideOptions = document.getElementById("options");

        for(var i =0; i<type.length;i++){
            if(type[i].checked){
                var ans = type[i].value;
                checkForChecked=true;
                hiddenDiv.style.display="block";
                DisabledButton.style.display="block";
                HideOptions.style.display="none";
            }
        }
        tosendData(ans);
    }
    </script>


    <style>
        #submit{
            display: none;
        }
        #hidden{
         display: none;  
         color: green;
        }
        section{
            display: flex;
            text-align: right;
            float: right;
            align-items: flex-start; 
        }
        span{
            text-align: center;
            color: red;
        }
        #id{
            background-color: blue;
            color: aliceblue;
        }
        .container{
            align-items: center;
        }
        .ques{
            width: auto;
            height: auto;
            background-color: blue;
            color: aliceblue;
        }
    </style>
</head>
<body>

<div class="col-lg-8 border border-sucess p-4 m-4 mx-auto">
    <section>
        <div class="container">
            <h3>Time Left : </h3><h3 id="count" style="border: 3px solid red;">15</h3>
        </div>
    </section>

        <!--Below code to inform user about the quiz-->
    <span><h3>*Once you click any option, it will hide the all options. So ANSWER CAREFULLY !!!</h3></span>
    {% for i in sciencequestions %} <!--code to retrive questions, options and answer by using for loop-->
    <br>
    <h1 class ="ques">Set 2 - Science Question</h1><br> <div class="container1"><h2>{{i.question}}</h2></div><br>
    <form>

    <div id="options"> 

        <div class="radio">
            <label><input type="radio" id="option1" name="name" value="{{i.option1}}" onclick="func()"><b> {{i.option1}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option2" name="name" value="{{i.option2}}" onclick="func()"><b> {{i.option2}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option3" name="name" value="{{i.option3}}" onclick="func()"><b> {{i.option3}}</b></label>
        </div>

        <div class="radio">
            <label><input type="radio" id="option4" name="name" value="{{i.option4}}" onclick="func()"><b> {{i.option4}}</b></label>
        </div>

    </div>
        <div id="hidden">
            <label><h2>Correct Answer is : {{i.answer}}</h2></label>
        </div>
        
        <br>
    </form>
    {% endfor %}

    <div class="paginator">
        <div class="form-group">
            {% if sciencequestions.has_next %}
                <a href="?page={{ sciencequestions.next_page_number }}"><button class="btn form-control btn-primary" id="submit">Next</button></a>
            {% else %}<!--below code take the user answers and show the score and user name-->
                <a href="/result/"><button class="btn form-control btn-success" id="submit">Submit</button></a>
            {% endif %}
        </div>
    </div>
</div>


</body>
</html>

---------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------RESULT PAGE CODE-------------------------------------------------------------

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <style>
        .container{
            text-align: center;
        }
        .name{
            background-color: blue;
            color: aliceblue;
        }
    </style>
</head>
<body>
    <div class="col-lg-8 border border-sucess p-4 m-4 mx-auto">
        <div class="container">
        <h1 class="name">Student Name : {{username}}</h1><!--to show user name-->
        <h1>
        Score : {{score}}<br><!--to show the score of the user name-->
        </div>
        <a href="/home/"><button class="btn form-control btn-success" id="submit">Start Page</button></a>
        </h1>
    </div>
</body>
</html>
------------------------------------------------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------MODELS.PY CODE FOR CREATING TABLES--------------------------------------------------

from django.db import models

# table to store questions, options and answers for the questions for second quiz
class ScienceQuestions(models.Model):
    question = models.CharField(max_length=100)

    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)    
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100)

    answer=models.CharField(max_length=100)


# table to store questions, options and answers for the questions for first quiz
class Questions(models.Model):
    question = models.CharField(max_length=100)

    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)    
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100)

    answer=models.CharField(max_length=100)


#table to store username and score
class User(models.Model):
    StudentName = models.CharField(max_length=50)
    Scores = models.IntegerField()
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------OTHERS ARE BASIC CODE IN DJANGO FRAMEWORKS---------------------------------------------------------------
