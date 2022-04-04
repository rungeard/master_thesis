from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Custome_questions_PDF(models.Model):
    class Meta: 
        verbose_name = "Custom question PDF"
        verbose_name_plural = "Custom questions PDF"
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    free_text = models.TextField(null=True)
        
class Custome_questions(models.Model):
    class Meta: 
        verbose_name = "Custom question AR"
        verbose_name_plural = "Custom questions AR"
        
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    age = models.CharField(
        choices=[
            ('1', '-20 '),
            ('2', '20 - 30'),
            ('3', '30 - 40'),
            ('4', '40 - 50'),
            ('5', '50 - 60'),
            ('6', '+60'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    experience = models.CharField(
        choices=[
            ('1', 'This is my first experience in augmented reality'),
            ('2', 'I had already experimented augmented reality'),
            ('3', 'I regularly use augmented reality'),
            (None, 'Not answered'),
        ],
        max_length=150,
        default=None,
        null=True,
    )
    discomfort = models.CharField(
        choices=[
            ('0', 'No'),
            ('1', 'Yes'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    daily_use = models.CharField(
        choices=[
            ('1', 'I would like it'),
            ('0', 'I would prefer a traditional method'),
            (None, 'Not answered'),
        ],
        max_length=50,
        default=None,
        null=True,
    )
    pause_use = models.CharField(
        choices=[
            ('0', 'No'),
            ('1', 'Yes'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    reverse_use = models.CharField(
        choices=[
            ('0', 'No'),
            ('1', 'Yes'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    pause_function = models.PositiveSmallIntegerField(null=True)
    speed = models.PositiveSmallIntegerField(null=True)
    visibility = models.PositiveSmallIntegerField(null=True)
    free_text = models.TextField(null=True)

    def complete(self):
        b = True 
        b *= self.age != None
        b *= self.experience != None
        b *= self.discomfort != None
        b *= self.daily_use != None
        b *= self.pause_function != None
        b *= self.pause_use != None
        b *= self.reverse_use != None
        b *= self.speed != None 
        b *= self.visibility != None
        return bool(b)
    
class Time_spend_AR(models.Model):
    class Meta: 
        verbose_name = "time spent for assembly in AR "
        verbose_name_plural = "times spent for assembly in AR "
        
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    beginn = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    def time_spent(self):
        return self.end-self.beginn
    def complete(self):
        return self.end != None and self.beginn != None

class Time_spend_PDF(models.Model):
    class Meta: 
        verbose_name = "time spent for assembly with a PDF guide "
        verbose_name_plural = "times spent for assembly with a PDF guide "
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    beginn = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    def time_spent(self):
        return self.end-self.beginn
    def complete(self):
        return self.end != None and self.beginn != None

class Assembly(models.Model):
    class Meta: 
        verbose_name = "Number of correct part per assembly"
        verbose_name_plural = "Numbers of correct part per assembly"
        
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    AR = models.PositiveSmallIntegerField(null=True)
    PDF = models.PositiveSmallIntegerField(null=True)
    def proportion_AR(self):
        return round((self.AR / 57)*100,2)

    def proportion_PDF(self):
        return round((self.PDF / 57)*100,2)

    def complete(self):
        return self.AR != None and self.PDF != None
           
class NASA_TLX_AR(models.Model):
    class Meta: 
        verbose_name = "answer to Nasa TLX survey for AR assembly"
        verbose_name_plural = "answers to Nasa TLX survey for AR assembly"
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    Mental_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Physical_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Temporal_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Performance_Rating = models.PositiveSmallIntegerField(null=True)
    Effort_Rating = models.PositiveSmallIntegerField(null=True)
    Frustration_Rating = models.PositiveSmallIntegerField(null=True)

    Effort_or_Performance = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Frustration = models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Effort =models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Effort', 'Effort'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Frustration = models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Performance_or_Frustration = models.CharField(
        choices=[
            ('Frustration', 'Frustration'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Temporal_Demand = models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Temporal Demand', 'Temporal Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Performance =models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Mental_Demand = models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Mental Demand', 'Mental Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Frustration_or_Effort = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Performance_or_Mental_Demand =models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    ) 
    Performance_or_Temporal_Demand =models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Mental_Demand_or_Effort = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Mental Demand', 'Mental Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Mental_Demand_or_Physical_Demand = models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Physical Demand', 'Physical Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Effort_or_Physical_Demand = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Physical Demand', 'Physical Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Frustration_or_Mental_Demand =models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )

    def Mental_Demand_Tally(self):
        c = 0
        if self.Temporal_Demand_or_Mental_Demand =='Mental Demand' :
            c+=1
        if self.Performance_or_Mental_Demand =='Mental Demand' :
            c+=1
        if self.Mental_Demand_or_Effort =='Mental Demand' :
            c+=1
        if self.Mental_Demand_or_Physical_Demand =='Mental Demand' :
            c+=1
        if self.Frustration_or_Mental_Demand =='Mental Demand' :
            c+=1
        return c
    
    def Physical_Demand_Tally(self):
        c = 0
        if self.Physical_Demand_or_Frustration =='Physical Demand' :
            c+=1
        if self.Physical_Demand_or_Temporal_Demand=='Physical Demand' :
            c+=1
        if self.Physical_Demand_or_Performance=='Physical Demand' :
            c+=1
        if self.Mental_Demand_or_Physical_Demand=='Physical Demand' :
            c+=1
        if self.Effort_or_Physical_Demand=='Physical Demand' :
            c+=1
        return c
        
    def Temporal_Demand_Tally(self):
        c = 0
        if self.Temporal_Demand_or_Mental_Demand=='Temporal Demand' :
            c+=1
        if self.Physical_Demand_or_Temporal_Demand=='Temporal Demand' :
            c+=1
        if self.Temporal_Demand_or_Frustration=='Temporal Demand' :
            c+=1
        if self.Temporal_Demand_or_Effort=='Temporal Demand' :
            c+=1
        if self.Performance_or_Temporal_Demand=='Temporal Demand' :
            c+=1
        return c
        
    def Performance_Tally(self):
        c = 0
        if self.Performance_or_Mental_Demand=='Performance' :
            c+=1
        if self.Physical_Demand_or_Performance=='Performance' :
            c+=1
        if self.Performance_or_Temporal_Demand=='Performance' :
            c+=1
        if self.Effort_or_Performance=='Performance' :
            c+=1
        if self.Performance_or_Frustration=='Performance' :
            c+=1
        return c
        
    def Effort_Tally(self):
        c = 0
        if self.Mental_Demand_or_Effort=='Effort' :
            c+=1
        if self.Effort_or_Physical_Demand=='Effort' :
            c+=1
        if self.Temporal_Demand_or_Effort=='Effort' :
            c+=1
        if self.Effort_or_Performance=='Effort' :
            c+=1
        if self.Frustration_or_Effort=='Effort' :
            c+=1        
        return c
        
    def Frustration_Tally(self):
        c = 0
        if self.Frustration_or_Mental_Demand=='Frustration' :
            c+=1
        if self.Physical_Demand_or_Frustration=='Frustration' :
            c+=1
        if self.Temporal_Demand_or_Frustration=='Frustration' :
            c+=1
        if self.Performance_or_Frustration=='Frustration' :
            c+=1
        if self.Frustration_or_Effort=='Frustration' :
            c+=1 
        return c

    def Mental_Demand_Weight(self):
        return self.Mental_Demand_Taily()/15
    def Physical_Demand_Weight(self):
        return self.Physical_Demand_Taily()/15
    def Temporal_Demand_Weight(self):
        return self.Temporal_Demand_Taily()/15
    def Performance_Weight(self):
        return self.Performance_Taily()/15
    def Effort_Weight(self):
        return self.Effort_Taily()/15
    def Frustration_Weight(self):
        return self.Frustration_Taily()/15

    def Overall(self):
        c=0
        c+= self.Mental_Demand_Rating*self.Mental_Demand_Tally()
        c+= self.Physical_Demand_Rating*self.Physical_Demand_Tally()
        c+= self.Temporal_Demand_Rating*self.Temporal_Demand_Tally()
        c+= self.Performance_Rating*self.Performance_Tally()
        c+= self.Effort_Rating*self.Effort_Tally()
        c+= self.Frustration_Rating*self.Frustration_Tally()
        return round(c/15,2)

    def complete(self):
        b = True 
        b *= self.Effort_or_Performance != None
        b *= self.Temporal_Demand_or_Frustration != None
        b *= self.Temporal_Demand_or_Effort != None
        b *= self.Physical_Demand_or_Frustration != None
        b *= self.Performance_or_Frustration != None
        b *= self.Physical_Demand_or_Temporal_Demand != None 
        b *= self.Physical_Demand_or_Performance != None
        b *= self.Temporal_Demand_or_Mental_Demand != None
        b *= self.Frustration_or_Effort != None
        b *= self.Performance_or_Mental_Demand != None
        b *= self.Performance_or_Temporal_Demand != None
        b *= self.Mental_Demand_or_Effort != None
        b *= self.Mental_Demand_or_Physical_Demand != None
        b *= self.Effort_or_Physical_Demand != None
        b *= self.Frustration_or_Mental_Demand != None
        return bool(b)

class SUS_AR(models.Model):
    class Meta: 
        verbose_name = "answer to SUS survey for AR assembly"
        verbose_name_plural = "answers to SUS survey for AR assembly"
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    question1 = models.PositiveSmallIntegerField(null=True)
    question2 = models.PositiveSmallIntegerField(null=True)
    question3 = models.PositiveSmallIntegerField(null=True)
    question4 = models.PositiveSmallIntegerField(null=True)
    question5 = models.PositiveSmallIntegerField(null=True)
    question6 = models.PositiveSmallIntegerField(null=True)
    question7 = models.PositiveSmallIntegerField(null=True)
    question8 = models.PositiveSmallIntegerField(null=True)
    question9 = models.PositiveSmallIntegerField(null=True)
    question10 = models.PositiveSmallIntegerField(null=True)

    def complete(self):
        b=True
        b *= self.question1 != None
        b *= self.question2 != None
        b *= self.question3 != None
        b *= self.question4 != None
        b *= self.question5 != None
        b *= self.question6 != None
        b *= self.question7 != None
        b *= self.question8 != None
        b *= self.question9 != None
        b *= self.question10 != None
        return bool(b)

class AS_AR(models.Model):
    class Meta: 
        verbose_name = "answer to after-study survey for AR assembly"
        verbose_name_plural = "answers to after-study survey for AR assembly"
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    question1 = models.PositiveSmallIntegerField(null=True)
    question2 = models.PositiveSmallIntegerField(null=True)
    question3 = models.PositiveSmallIntegerField(null=True)

    def complete(self):
        b=True
        b *= self.question1 != None
        b *= self.question2 != None
        b *= self.question3 != None
        return bool(b)

class NASA_TLX_PDF(models.Model):
    class Meta: 
        verbose_name = "answer to Nasa TLX survey for assembly with a PDF guide"
        verbose_name_plural = "answers to Nasa TLX survey for assembly with a PDF guide"
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)

    Mental_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Physical_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Temporal_Demand_Rating = models.PositiveSmallIntegerField(null=True)
    Performance_Rating = models.PositiveSmallIntegerField(null=True)
    Effort_Rating = models.PositiveSmallIntegerField(null=True)
    Frustration_Rating = models.PositiveSmallIntegerField(null=True)

    Effort_or_Performance = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Frustration = models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Effort =models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Effort', 'Effort'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Frustration = models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Performance_or_Frustration = models.CharField(
        choices=[
            ('Frustration', 'Frustration'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Temporal_Demand = models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Temporal Demand', 'Temporal Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Physical_Demand_or_Performance =models.CharField(
        choices=[
            ('Physical Demand', 'Physical Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Temporal_Demand_or_Mental_Demand = models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Mental Demand', 'Mental Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Frustration_or_Effort = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Performance_or_Mental_Demand =models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    ) 
    Performance_or_Temporal_Demand =models.CharField(
        choices=[
            ('Temporal Demand', 'Temporal Demand'),
            ('Performance', 'Performance'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Mental_Demand_or_Effort = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Mental Demand', 'Mental Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Mental_Demand_or_Physical_Demand = models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Physical Demand', 'Physical Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Effort_or_Physical_Demand = models.CharField(
        choices=[
            ('Effort', 'Effort'),
            ('Physical Demand', 'Physical Demand'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )
    Frustration_or_Mental_Demand =models.CharField(
        choices=[
            ('Mental Demand', 'Mental Demand'),
            ('Frustration', 'Frustration'),
            (None, 'Not answered'),
        ],
        max_length=20,
        default=None,
        null=True,
    )

    def Mental_Demand_Tally(self):
        c = 0
        if self.Temporal_Demand_or_Mental_Demand =='Mental Demand' :
            c+=1
        if self.Performance_or_Mental_Demand =='Mental Demand' :
            c+=1
        if self.Mental_Demand_or_Effort =='Mental Demand' :
            c+=1
        if self.Mental_Demand_or_Physical_Demand =='Mental Demand' :
            c+=1
        if self.Frustration_or_Mental_Demand =='Mental Demand' :
            c+=1
        return c
    
    def Physical_Demand_Tally(self):
        c = 0
        if self.Physical_Demand_or_Frustration =='Physical Demand' :
            c+=1
        if self.Physical_Demand_or_Temporal_Demand=='Physical Demand' :
            c+=1
        if self.Physical_Demand_or_Performance=='Physical Demand' :
            c+=1
        if self.Mental_Demand_or_Physical_Demand=='Physical Demand' :
            c+=1
        if self.Effort_or_Physical_Demand=='Physical Demand' :
            c+=1
        return c
        
    def Temporal_Demand_Tally(self):
        c = 0
        if self.Temporal_Demand_or_Mental_Demand=='Temporal Demand' :
            c+=1
        if self.Physical_Demand_or_Temporal_Demand=='Temporal Demand' :
            c+=1
        if self.Temporal_Demand_or_Frustration=='Temporal Demand' :
            c+=1
        if self.Temporal_Demand_or_Effort=='Temporal Demand' :
            c+=1
        if self.Performance_or_Temporal_Demand=='Temporal Demand' :
            c+=1
        return c
        
    def Performance_Tally(self):
        c = 0
        if self.Performance_or_Mental_Demand=='Performance' :
            c+=1
        if self.Physical_Demand_or_Performance=='Performance' :
            c+=1
        if self.Performance_or_Temporal_Demand=='Performance' :
            c+=1
        if self.Effort_or_Performance=='Performance' :
            c+=1
        if self.Performance_or_Frustration=='Performance' :
            c+=1
        return c
        
    def Effort_Tally(self):
        c = 0
        if self.Mental_Demand_or_Effort=='Effort' :
            c+=1
        if self.Effort_or_Physical_Demand=='Effort' :
            c+=1
        if self.Temporal_Demand_or_Effort=='Effort' :
            c+=1
        if self.Effort_or_Performance=='Effort' :
            c+=1
        if self.Frustration_or_Effort=='Effort' :
            c+=1        
        return c
        
    def Frustration_Tally(self):
        c = 0
        if self.Frustration_or_Mental_Demand=='Frustration' :
            c+=1
        if self.Physical_Demand_or_Frustration=='Frustration' :
            c+=1
        if self.Temporal_Demand_or_Frustration=='Frustration' :
            c+=1
        if self.Performance_or_Frustration=='Frustration' :
            c+=1
        if self.Frustration_or_Effort=='Frustration' :
            c+=1 
        return c

    def Mental_Demand_Weight(self):
        return self.Mental_Demand_Taily()/15
    def Physical_Demand_Weight(self):
        return self.Physical_Demand_Taily()/15
    def Temporal_Demand_Weight(self):
        return self.Temporal_Demand_Taily()/15
    def Performance_Weight(self):
        return self.Performance_Taily()/15
    def Effort_Weight(self):
        return self.Effort_Taily()/15
    def Frustration_Weight(self):
        return self.Frustration_Taily()/15

    def Overall(self):
        c=0
        c+= self.Mental_Demand_Rating*self.Mental_Demand_Tally()
        c+= self.Physical_Demand_Rating*self.Physical_Demand_Tally()
        c+= self.Temporal_Demand_Rating*self.Temporal_Demand_Tally()
        c+= self.Performance_Rating*self.Performance_Tally()
        c+= self.Effort_Rating*self.Effort_Tally()
        c+= self.Frustration_Rating*self.Frustration_Tally()
        return round(c/15,2)

    def complete(self):
        b = True 
        b *= self.Effort_or_Performance != None
        b *= self.Temporal_Demand_or_Frustration != None
        b *= self.Temporal_Demand_or_Effort != None
        b *= self.Physical_Demand_or_Frustration != None
        b *= self.Performance_or_Frustration != None
        b *= self.Physical_Demand_or_Temporal_Demand != None 
        b *= self.Physical_Demand_or_Performance != None
        b *= self.Temporal_Demand_or_Mental_Demand != None
        b *= self.Frustration_or_Effort != None
        b *= self.Performance_or_Mental_Demand != None
        b *= self.Performance_or_Temporal_Demand != None
        b *= self.Mental_Demand_or_Effort != None
        b *= self.Mental_Demand_or_Physical_Demand != None
        b *= self.Effort_or_Physical_Demand != None
        b *= self.Frustration_or_Mental_Demand != None
        return bool(b)
    
    

class SUS_PDF(models.Model):
    class Meta: 
        verbose_name = "answer to SUS survey for assembly with a PDF guide"
        verbose_name_plural = "answers to SUS survey for assembly with a PDF guide"
        
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    question1 = models.PositiveSmallIntegerField(null=True)
    question2 = models.PositiveSmallIntegerField(null=True)
    question3 = models.PositiveSmallIntegerField(null=True)
    question4 = models.PositiveSmallIntegerField(null=True)
    question5 = models.PositiveSmallIntegerField(null=True)
    question6 = models.PositiveSmallIntegerField(null=True)
    question7 = models.PositiveSmallIntegerField(null=True)
    question8 = models.PositiveSmallIntegerField(null=True)
    question9 = models.PositiveSmallIntegerField(null=True)
    question10 = models.PositiveSmallIntegerField(null=True)

    def complete(self):
        b=True
        b *= self.question1 != None
        b *= self.question2 != None
        b *= self.question3 != None
        b *= self.question4 != None
        b *= self.question5 != None
        b *= self.question6 != None
        b *= self.question7 != None
        b *= self.question8 != None
        b *= self.question9 != None
        b *= self.question10 != None
        return bool(b)

class AS_PDF(models.Model):
    class Meta: 
        verbose_name = "answer to after-study survey for assembly with a PDF guide"
        verbose_name_plural = "answers to after-study survey for assembly with a PDF guide"
        
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    question1 = models.PositiveSmallIntegerField(null=True)
    question2 = models.PositiveSmallIntegerField(null=True)
    question3 = models.PositiveSmallIntegerField(null=True)

    def complete(self):
        b=True
        b *= self.question1 != None
        b *= self.question2 != None
        b *= self.question3 != None
        return bool(b)
