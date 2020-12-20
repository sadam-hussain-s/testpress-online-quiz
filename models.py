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
