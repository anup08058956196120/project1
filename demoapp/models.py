from django.db import models

# Create your models here.

class Examportal(models.Model):
     name=models.CharField(max_length=20,primary_key=True)
     password=models.CharField(max_length=20)
     mobno = models.IntegerField()
     email=models.CharField(max_length=100)
     

     #__str__() function gives us object data .

     def __str__(self):
          return "{},{},{},{}".format(self.name,self.password,self.mobno,self.email)

     class Meta:
          db_table="exam" 
          
          
 
class Questions(models.Model):
     qno = models.IntegerField(primary_key=True)
     qtext=models.CharField(max_length=300)
     qanswer=models.CharField(max_length=100)
     op1=models.CharField(max_length=100)
     op2=models.CharField(max_length=100)
     subject=models.CharField(max_length=50)
     def __str__(self):
           return "{},{},{},{},{},{}".format(self.qno,self.qtext,self.qanswer,self.op1,self.op2,self.subject)

     class Meta:
          db_table="questions" 
          
          
class Score(models.Model):
     name=models.CharField(max_length=50,primary_key=True)
     subject=models.CharField(max_length=50)
     score=models.IntegerField()
     
     def __str__(self):
           return "{},{},{}".format(self.name,self.subject,self.score)
     
     class Meta:
          db_table="score"