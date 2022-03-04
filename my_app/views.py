from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import datetime
import csv
import random
import string

nasa_tlx_dic = {
    "Mental Demand":"How much mental and perceptual activity was required (e.g. thinking, deciding, calculating, remembering, looking, searching, etc)? Was the task easy or demanding, simple or complex, exacting or forgiving?",
    "Physical Demand":"How much physical activity was required (e.g. pushing, pulling, turning, controlling, activating, etc)? Was the task easy or demanding, slow or brisk, slack or strenuous, restful or laborious?",
    "Temporal Demand":"How much time pressure did you feel due to the rate of pace at which the tasks or task elements occurred? Was the pace slow and leisurely or rapid and frantic?",
    "Performance":"How successful do you think you were in accomplishing the goals of the task set by the experimenter (or yourself)? How satisfied were you with your performance in accomplishing these goals?",
    "Effort":"How hard did you have to work (mentally and physically) to accomplish your level of performance?",
    "Frustration":"How insecure, discouraged, irritated, stressed and annoyed versus secure, gratified, content, relaxed and complacent did you feel during the task?"
}

SUS_dic = {"question1":"I think that I would like to use this system frequently",
           "question2":"I found the system unnecessarily complex.",
           "question3":"I thought the system was easy to use.",
           "question4":"I think that I would need the support of a technical person to be able to use this system.",
           "question5":"I found the various functions in this system were well integrated.",
           "question6":"I thought there was too much inconsistency in this system.",
           "question7":"I would imagine that most people would learn to use this system very quickly.",
           "question8":"I found the system very cumbersome/awkward to use.",
           "question9":"I felt very confident using the system.",
           "question10":"I needed to learn a lot of things before I could get going with this system."
}

AS_dic = {"question1":"Overall, I am satisfied with the ease of completing the tasks in this scenario",
          "question2":"Overall, I am satisfied with the amount of time it took to complete the tasks in this scenario ",
          "question3":"Overall, I am satisfied with the support information (online-line help, messages, documentation) when completing the tasks",
}

def complete_study(user):
    complete_task3 = Time_spend_PDF.objects.filter(user = user).exists() and Time_spend_PDF.objects.get(user = user).complete()
    complete_task1 = Time_spend_AR.objects.filter(user = user).exists() and Time_spend_AR.objects.get(user = user).complete()
    
        
    complete_task2=False
    complete_subtask2= NASA_TLX_AR.objects.filter(user = user).exists() and NASA_TLX_AR.objects.get(user = user).complete()
    complete_subtask2 *= SUS_AR.objects.filter(user = user).exists() and SUS_AR.objects.get(user = user).complete()
    complete_subtask2 *= AS_AR.objects.filter(user = user).exists() and AS_AR.objects.get(user = user).complete()
    complete_subtask2 *= Custome_questions.objects.filter(user = user).exists() and Custome_questions.objects.get(user = user).complete()
    complete_task2 += complete_subtask2

    complete_task4=False
    complete_subtask4= NASA_TLX_PDF.objects.filter(user = user).exists() and NASA_TLX_PDF.objects.get(user = user).complete()
    complete_subtask4 *= SUS_PDF.objects.filter(user = user).exists() and SUS_PDF.objects.get(user = user).complete()
    complete_subtask4 *= AS_PDF.objects.filter(user = user).exists() and AS_PDF.objects.get(user = user).complete()
    complete_task4 += complete_subtask4

    complete = complete_task1 * complete_task2 * complete_task3 * complete_task4
    return (complete_task1, complete_task2, complete_task3, complete_task4, complete)

# Create your views here.
def index(request):
    return render(request, 'my_app/index.html')

def register(request):
    if request.method == "POST":
        form = Register_form(request.POST)
        if form.is_valid():
            name = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
            password = form.cleaned_data["password"]
            while User.objects.filter(username=name).exists():
                name = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
            User.objects.create_user(name, None, password)
            user = authenticate(request, username=name, password=password) 
            if user: 
                dj_login(request, user) 
                return redirect('welcome_new')
    else:
        form = Register_form()
    return render(request, 'my_app/register.html', locals())

def login(request):
    error = False
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=name, password=password) 
            if user: 
                dj_login(request, user) 
                return redirect('welcome')
            else: 
                error = True
    else:
        form = Login_form()
    return render(request, 'my_app/login.html', locals())

@login_required
def logout(request):
    dj_logout(request)
    return redirect('login')

@login_required
def welcome(request, first_connection=False):
    complete_task1 = complete_study(request.user)[0]
    complete_task2 = complete_study(request.user)[1]
    complete_task3 = complete_study(request.user)[2]
    complete_task4 = complete_study(request.user)[3]
    complete = complete_study(request.user)[4]
    if complete_task3:
        time_task3 = Time_spend_PDF.objects.get(user = request.user).time_spent()
    if complete_task1:
        time_task1 = Time_spend_AR.objects.get(user = request.user).time_spent()
    return render(request, 'my_app/welcome.html', locals())

@login_required
def task1(request, start):
    if start > 1:
        return redirect('welcome')
    elif Time_spend_AR.objects.filter(user = request.user).exists() and Time_spend_AR.objects.get(user = request.user).complete():
        return redirect('welcome')
    elif start == 0:
        time = Time_spend_AR(user = request.user, beginn=datetime.today())
        time.save()
        return render(request, 'my_app/task1.html')
    elif start == 1:
        time = Time_spend_AR.objects.get(user = request.user)
        time.end = datetime.today()
        time.save()
        return redirect('welcome')

@login_required
def task21(request, nasa_tlx_dic=nasa_tlx_dic, AR=True):
    if AR :
        task = "AR Assembly"
        id_path = "2"
        if not NASA_TLX_AR.objects.filter(user = request.user).exists():
            nasa_tlx = NASA_TLX_AR(user = request.user)
            nasa_tlx.save()
        else:
            nasa_tlx = NASA_TLX_AR.objects.get(user = request.user)
    else:
        task = "Assembly with a PDF guide"
        id_path = "4"
        if not NASA_TLX_PDF.objects.filter(user = request.user).exists():
            nasa_tlx = NASA_TLX_PDF(user = request.user)
            nasa_tlx.save()
        else:
            nasa_tlx = NASA_TLX_PDF.objects.get(user = request.user)
    if nasa_tlx.complete():
        return redirect('/task%s/part3'%id_path)
    if request.method == "POST":                
        nasa_tlx.Mental_Demand_Rating = int(request.POST['Mental Demand'])
        nasa_tlx.Physical_Demand_Rating = int(request.POST['Physical Demand'])
        nasa_tlx.Temporal_Demand_Rating = int(request.POST['Temporal Demand'])
        nasa_tlx.Performance_Rating = int(request.POST['Performance'])
        nasa_tlx.Effort_Rating = int(request.POST['Effort'])
        nasa_tlx.Frustration_Rating = int(request.POST['Frustration'])
        nasa_tlx.save()
        return redirect('/task%s/part2/0'%id_path)

    return render(request, 'my_app/survey1.html',locals())

@login_required
def task22(request, id_question, answer=None, nasa_tlx_dic=nasa_tlx_dic, AR=True):
    if id_question > 14:
        return redirect('index')
    if AR:
        task = "AR Assembly"
        id_path = "2"
        if not NASA_TLX_AR.objects.filter(user = request.user).exists():
            nasa_tlx = NASA_TLX_AR(user = request.user)
            nasa_tlx.save()
        else:
            nasa_tlx = NASA_TLX_AR.objects.get(user = request.user)
    else :
        task = "Assembly with a PDF guide"
        id_path = "4"
        if not NASA_TLX_PDF.objects.filter(user = request.user).exists():
            nasa_tlx = NASA_TLX_PDF(user = request.user)
            nasa_tlx.save()
        else:
            nasa_tlx = NASA_TLX_PDF.objects.get(user = request.user)
    if nasa_tlx.complete():
        return redirect('/task%s/part3'%id_path)
    elif request.method == "POST":
        if id_question == 0 and answer in ['Effort','Performance'] :
            nasa_tlx.Effort_or_Performance = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/1'%id_path)
        elif id_question == 1 and answer in ['Temporal Demand','Frustration'] :
            nasa_tlx.Temporal_Demand_or_Frustration = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/2'%id_path)
        elif id_question == 2 and answer in ['Temporal Demand','Effort'] :
            nasa_tlx.Temporal_Demand_or_Effort = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/3'%id_path)
        elif id_question == 3 and answer in ['Physical Demand','Frustration'] :
            nasa_tlx.Physical_Demand_or_Frustration = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/4'%id_path)
        elif id_question == 4 and answer in ['Performance','Frustration'] :
            nasa_tlx.Performance_or_Frustration = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/5'%id_path)
        elif id_question == 5 and answer in ['Physical Demand','Temporal Demand'] :
            nasa_tlx.Physical_Demand_or_Temporal_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/6'%id_path)
        elif id_question == 6 and answer in ['Physical Demand','Performance'] :
            nasa_tlx.Physical_Demand_or_Performance = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/7'%id_path)
        elif id_question == 7 and answer in ['Temporal Demand','Mental Demand'] :
            nasa_tlx.Temporal_Demand_or_Mental_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/8'%id_path)
        elif id_question == 8 and answer in ['Effort','Frustration'] :
            nasa_tlx.Frustration_or_Effort = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/9'%id_path)
        elif id_question == 9 and answer in ['Mental Demand','Performance'] :
            nasa_tlx.Performance_or_Mental_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/10'%id_path)
        elif id_question == 10 and answer in ['Temporal Demand','Performance'] :
            nasa_tlx.Performance_or_Temporal_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/11'%id_path)
        elif id_question == 11 and answer in ['Effort','Mental Demand'] :
            nasa_tlx.Mental_Demand_or_Effort = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/12'%id_path)
        elif id_question == 12 and answer in ['Mental Demand','Physical Demand'] :
            nasa_tlx.Mental_Demand_or_Physical_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/13'%id_path)
        elif id_question == 13 and answer in ['Effort','Physical Demand'] :
            nasa_tlx.Effort_or_Physical_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part2/14'%id_path)
        elif id_question == 14 and answer in ['Frustration','Mental Demand'] :
            nasa_tlx.Frustration_or_Mental_Demand = answer
            nasa_tlx.save()
            return redirect('/task%s/part3'%id_path)
    else:
        if id_question == 0:
            item1 = "Effort"
            description1 = nasa_tlx_dic[item1]
            item2 = "Performance"
            description2 = nasa_tlx_dic[item2]
            complete = "21"
        
        elif id_question == 1:
            item1 = "Temporal Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Frustration"
            description2 = nasa_tlx_dic[item2]
            complete = "24"

        elif id_question == 2:
            item1 = "Temporal Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Effort"
            description2 = nasa_tlx_dic[item2]
            complete = "27"

        elif id_question == 3:
            item1 = "Physical Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Frustration"
            description2 = nasa_tlx_dic[item2]
            complete = "30"
            
        elif id_question == 4:
            item1 = "Performance"
            description1 = nasa_tlx_dic[item1]
            item2 = "Frustration"
            description2 = nasa_tlx_dic[item2]
            complete = "33"

        elif id_question == 5:
            item1 = "Physical Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Temporal Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "36"

        elif id_question == 6:
            item1 = "Physical Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Performance"
            description2 = nasa_tlx_dic[item2]
            complete = "39"
            
        elif id_question == 7:
            item1 = "Temporal Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Mental Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "42"
            
        elif id_question == 8:
            item1 = "Frustration"
            description1 = nasa_tlx_dic[item1]
            item2 = "Effort"
            description2 = nasa_tlx_dic[item2]
            complete = "45"
            
        elif id_question == 9:
            item1 = "Performance"
            description1 = nasa_tlx_dic[item1]
            item2 = "Mental Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "48"
            
        elif id_question == 10:
            item1 = "Performance"
            description1 = nasa_tlx_dic[item1]
            item2 = "Temporal Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "51"
            
        elif id_question == 11:
            item1 = "Mental Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Effort"
            description2 = nasa_tlx_dic[item2]
            complete = "54"

        elif id_question == 12:
            item1 = "Mental Demand"
            description1 = nasa_tlx_dic[item1]
            item2 = "Physical Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "57"
            
        elif id_question == 13:
            item1 = "Effort"
            description1 = nasa_tlx_dic[item1]
            item2 = "Physical Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "60"
            
        elif id_question == 14:
            item1 = "Frustration"
            description1 = nasa_tlx_dic[item1]
            item2 = "Mental Demand"
            description2 = nasa_tlx_dic[item2]
            complete = "63"
        
    return render(request, 'my_app/survey2.html',locals())

@login_required
def task23(request, SUS_dic=SUS_dic, AR=True):
    if AR :
        task = "AR Assembly"
        id_path = "2"
        if not SUS_AR.objects.filter(user = request.user).exists():
            sus = SUS_AR(user = request.user)
            sus.save()
        else:
            sus = SUS_AR.objects.get(user = request.user)
    else :
        task = "Assembly with a PDF guide"
        id_path = "4"
        if not SUS_PDF.objects.filter(user = request.user).exists():
            sus = SUS_PDF(user = request.user)
            sus.save()
        else:
            sus = SUS_PDF.objects.get(user = request.user)
    if sus.complete():
        return redirect('/task%s/part4'%id_path)
    if request.method == "POST":
        sus.question1 = int(request.POST['question1'])
        sus.question2 = int(request.POST['question2'])
        sus.question3 = int(request.POST['question3'])
        sus.question4 = int(request.POST['question4'])
        sus.question5 = int(request.POST['question5'])
        sus.question6 = int(request.POST['question6'])
        sus.question7 = int(request.POST['question7'])
        sus.question8 = int(request.POST['question8'])
        sus.question9 = int(request.POST['question9'])
        sus.question10 = int(request.POST['question10'])
        sus.save()
        return redirect('/task%s/part4'%id_path)

    return render(request, 'my_app/survey3.html', locals())

@login_required
def task24(request, AS_dic = AS_dic, AR = True):
    if AR:
        task = "AR Assembly"
        id_path = "2"
        if not AS_AR.objects.filter(user = request.user).exists():
            aso = AS_AR(user = request.user)
            aso.save()
        else:
            aso = AS_AR.objects.get(user = request.user)
    else :
        task = "Assembly with a PDF guide"
        id_path = "4"
        if not AS_PDF.objects.filter(user = request.user).exists():
            aso = AS_PDF(user = request.user)
            aso.save()
        else:
            aso = AS_PDF.objects.get(user = request.user)
    if aso.complete():
        if AR :
            return redirect('task25')
        else:
            return redirect('welcome')
    if request.method == "POST":       
        aso.question1 = int(request.POST['question1'])
        aso.question2 = int(request.POST['question2'])
        aso.question3 = int(request.POST['question3'])
        aso.save()
        if AR :
            return redirect('task25')
        else:
            return redirect('welcome')
    return render(request, 'my_app/survey4.html', locals())

@login_required
def task25(request):
    if not Custome_questions.objects.filter(user = request.user).exists():
        c = Custome_questions(user = request.user)
        c.save()
    else:
        c = Custome_questions.objects.get(user = request.user)

    if c.complete():
        return redirect('welcome')

    if request.method == "POST":
        c.age = request.POST['age']
        c.experience = request.POST['experience']
        c.discomfort = request.POST['discomfort']
        c.daily_use = request.POST['daily_use']
        c.pause_function = int(request.POST['pause_function'])
        c.speed = int(request.POST['speed'])
        c.visibility = int(request.POST['visibility'])
        c.free_text = request.POST['free_text'].replace(',',';')
        c.save()
        
        return redirect('welcome')
    
    return render(request, 'my_app/survey5.html', locals())

@login_required
def task3(request, start):
    if start > 1:
        return redirect('welcome')
    elif Time_spend_PDF.objects.filter(user = request.user).exists() and Time_spend_PDF.objects.get(user = request.user).complete():
        return redirect('welcome')
    elif start == 0:
        time = Time_spend_PDF(user = request.user, beginn=datetime.today())
        time.save()
        return render(request, 'my_app/task3.html')
    elif start == 1:
        time = Time_spend_PDF.objects.get(user = request.user)
        time.end = datetime.today()
        time.save()
        return redirect('welcome')

@login_required
def results(request, SUS_dic=SUS_dic, AS_dic=AS_dic):
    if not complete_study(request.user)[4] :
        return redirect('welcome')
        
    list_time_ar = [];
    for t in Time_spend_AR.objects.all():
        if t.complete():
            list_time_ar.append(t.time_spent().total_seconds())

    list_time_pdf = [];
    for t in Time_spend_PDF.objects.all():
        if t.complete():
            list_time_pdf.append(t.time_spent().total_seconds())

    list_nasa_tlx_ar =[]
    for n in NASA_TLX_AR.objects.all():
        if n.complete():
            list_nasa_tlx_ar.append(n.Overall())

    list_nasa_tlx_pdf =[]
    for n in NASA_TLX_PDF.objects.all():
        if n.complete():
            list_nasa_tlx_pdf.append(n.Overall())

    list_parts_ar=[]
    list_parts_pdf=[]
    for n in Assembly.objects.all():
        if n.complete():
            list_parts_ar.append(n.proportion_AR())
            list_parts_pdf.append(n.proportion_PDF())

    dic_sus_ar = {}
    dic_sus_pdf = {}
    
    for x in [1,2,3,4,5,6,7]:
        dic_sus_ar[str(x)]=[]
        dic_sus_pdf[str(x)]=[]
        
    for x in [1,2,3,4,5]:
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question1=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question1=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question2=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question2=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question3=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question3=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question4=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question4=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question5=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question5=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question6=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question6=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question7=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question7=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question8=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question8=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question9=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question9=x).count())
        dic_sus_ar[str(x)].append(SUS_AR.objects.filter(question10=x).count())
        dic_sus_pdf[str(x)].append(SUS_PDF.objects.filter(question10=x).count())

    dic_as_ar = {}
    dic_as_pdf = {}
    
    for x in [1,2,3]:
        dic_as_ar[str(x)]=[]
        dic_as_pdf[str(x)]=[]
        
    for x in [1,2,3,4,5,6,7]:
        dic_as_ar[str(1)].append(AS_AR.objects.filter(question1=x).count())
        dic_as_pdf[str(1)].append(AS_PDF.objects.filter(question1=x).count())
        dic_as_ar[str(2)].append(AS_AR.objects.filter(question2=x).count())
        dic_as_pdf[str(2)].append(AS_PDF.objects.filter(question2=x).count())
        dic_as_ar[str(3)].append(AS_AR.objects.filter(question3=x).count())
        dic_as_pdf[str(3)].append(AS_PDF.objects.filter(question3=x).count())

    dic_custom = {}
    for x in ['age','experience','method','pause','speed','visibility']:
        dic_custom[str(x)]=[]

    for x in [1,2,3,4,5,6]:
        dic_custom['age'].append(Custome_questions.objects.filter(age=str(x)).count())

    for x in [1,2,3]:
        dic_custom['experience'].append(Custome_questions.objects.filter(experience=str(x)).count())

    for x in [0,1]:
        dic_custom['method'].append(Custome_questions.objects.filter(daily_use=str(x)).count())

    for x in [1,2,3,4,5]:
        dic_custom['pause'].append(Custome_questions.objects.filter(pause_function=x).count())
        dic_custom['speed'].append(Custome_questions.objects.filter(speed=x).count())
        dic_custom['visibility'].append(Custome_questions.objects.filter(visibility=x).count())
        
        
    return render(request, 'my_app/results.html', locals())

@login_required
def csv_results(request):
    if not complete_study(request.user)[4] :
        return redirect('index')
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="results.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['user_id',
                     'time spent AR (in s)',
                     'nasa tlx mental demand rating AR',
                     'nasa tlx mental demand tally AR',
                     'nasa tlx physical demand rating AR',
                     'nasa tlx physical demand tally AR',
                     'nasa tlx temporal demand rating AR',
                     'nasa tlx temporal demand tally AR',
                     'nasa tlx performance rating AR',
                     'nasa tlx performance tally AR',
                     'nasa tlx effort rating AR',
                     'nasa tlx effort tally AR',
                     'nasa tlx frustration rating AR',
                     'nasa tlx frustration tally AR',
                     'nasa tlx overall rating AR',
                     'sus question 1 AR',
                     'sus question 2 AR',
                     'sus question 3 AR',
                     'sus question 4 AR',
                     'sus question 5 AR',
                     'sus question 6 AR',
                     'sus question 7 AR',
                     'sus question 8 AR',
                     'sus question 9 AR',
                     'sus question 10 AR',
                     'as question 1 AR',
                     'as question 2 AR',
                     'as question 3 AR',
                     'time spent PDF (in s)',
                     'nasa tlx mental demand rating PDF',
                     'nasa tlx mental demand tally PDF',
                     'nasa tlx physical demand rating PDF',
                     'nasa tlx physical demand tally PDF',
                     'nasa tlx temporal demand rating PDF',
                     'nasa tlx temporal demand tally PDF',
                     'nasa tlx performance rating PDF',
                     'nasa tlx performance tally PDF',
                     'nasa tlx effort rating PDF',
                     'nasa tlx effort tally PDF',
                     'nasa tlx frustration rating PDF',
                     'nasa tlx frustration tally PDF',
                     'nasa tlx overall rating PDF',
                     'sus question 1 PDF',
                     'sus question 2 PDF',
                     'sus question 3 PDF',
                     'sus question 4 PDF',
                     'sus question 5 PDF',
                     'sus question 6 PDF',
                     'sus question 7 PDF',
                     'sus question 8 PDF',
                     'sus question 9 PDF',
                     'sus question 10 PDF',
                     'as question 1 PDF',
                     'as question 2 PDF',
                     'as question 3 PDF',
                     'age group',
                     'experience',
                     'discomfort',
                     'daily_use',
                     'pause_function',
                     'speed',
                     'visibility',
                     'free_text',
                     'number of correct parts in AR',
                     'number of correct parts with PDF'
                     
    ])
    for u in User.objects.all():
        if complete_study(u)[4] :
            t_ar = Time_spend_AR.objects.get(user=u)
            t_pdf = Time_spend_PDF.objects.get(user=u)
            nasa_tlx_ar = NASA_TLX_AR.objects.get(user=u)
            nasa_tlx_pdf = NASA_TLX_PDF.objects.get(user=u)
            sus_ar = SUS_AR.objects.get(user=u)
            sus_pdf = SUS_PDF.objects.get(user=u)
            as_ar = AS_AR.objects.get(user=u)
            as_pdf = AS_PDF.objects.get(user=u)
            c = Custome_questions.objects.get(user=u)
            l = ['','']
            if Assembly.objects.filter(user=u).exists():
                assembly = Assembly.objects.get(user=u)
                l = [assembly.AR,assembly.PDF]
            writer.writerow([u.id,
                             t_ar.time_spent().total_seconds(),
                             nasa_tlx_ar.Mental_Demand_Rating,
                             nasa_tlx_ar.Mental_Demand_Tally(),
                             nasa_tlx_ar.Physical_Demand_Rating,
                             nasa_tlx_ar.Physical_Demand_Tally(),
                             nasa_tlx_ar.Temporal_Demand_Rating,
                             nasa_tlx_ar.Temporal_Demand_Tally(),
                             nasa_tlx_ar.Performance_Rating,
                             nasa_tlx_ar.Performance_Tally(),
                             nasa_tlx_ar.Effort_Rating,
                             nasa_tlx_ar.Effort_Tally(),
                             nasa_tlx_ar.Frustration_Rating,
                             nasa_tlx_ar.Frustration_Tally(),
                             nasa_tlx_ar.Overall(),
                             sus_ar.question1,
                             sus_ar.question2,
                             sus_ar.question3,
                             sus_ar.question4,
                             sus_ar.question5,
                             sus_ar.question6,
                             sus_ar.question7,
                             sus_ar.question8,
                             sus_ar.question9,
                             sus_ar.question10,
                             as_ar.question1,
                             as_ar.question2,
                             as_ar.question3,
                             t_pdf.time_spent().total_seconds(),
                             nasa_tlx_pdf.Mental_Demand_Rating,
                             nasa_tlx_pdf.Mental_Demand_Tally(),
                             nasa_tlx_pdf.Physical_Demand_Rating,
                             nasa_tlx_pdf.Physical_Demand_Tally(),
                             nasa_tlx_pdf.Temporal_Demand_Rating,
                             nasa_tlx_pdf.Temporal_Demand_Tally(),
                             nasa_tlx_pdf.Performance_Rating,
                             nasa_tlx_pdf.Performance_Tally(),
                             nasa_tlx_pdf.Effort_Rating,
                             nasa_tlx_pdf.Effort_Tally(),
                             nasa_tlx_pdf.Frustration_Rating,
                             nasa_tlx_pdf.Frustration_Tally(),
                             nasa_tlx_pdf.Overall(),
                             sus_pdf.question1,
                             sus_pdf.question2,
                             sus_pdf.question3,
                             sus_pdf.question4,
                             sus_pdf.question5,
                             sus_pdf.question6,
                             sus_pdf.question7,
                             sus_pdf.question8,
                             sus_pdf.question9,
                             sus_pdf.question10,
                             as_pdf.question1,
                             as_pdf.question2,
                             as_pdf.question3,
                             c.age,
                             c.experience,
                             c.discomfort,
                             c.daily_use,
                             c.pause_function,
                             c.speed,
                             c.visibility,
                             c.free_text
            ]+l)
            
    return response
