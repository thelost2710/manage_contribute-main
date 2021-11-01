from django.contrib.auth.models import User
from login.views import getAuthGroup
from staff.models import Contribution, Faculty, Type, Term, Comment, Like
from django.shortcuts import render, redirect
from django.db import connection, connections
from datetime import date
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        faculty = Faculty.objects.all()
        dasboard = []
        contribute = []
        for i in faculty:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM staff_contribution INNER JOIN staff_user ON staff_contribution.UserID_id = staff_user.id INNER JOIN staff_faculty ON staff_user.Faculty_id = staff_faculty.id WHERE staff_faculty.Name = %s", [i.Name])
                auth_group = cursor.fetchall()
            dasboard.append([i.Name, len(auth_group)])
        for i in faculty:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT staff_faculty.Name FROM staff_contribution INNER JOIN staff_user ON staff_contribution.UserID_id = staff_user.id INNER JOIN staff_faculty ON staff_user.Faculty_id = staff_faculty.id WHERE staff_faculty.Name = %s", [i.Name])
                contribute1 = cursor.fetchall()
            contribute.append([i.Name, len(contribute1)])
        print(contribute)
        data = {"dasboard": dasboard, "contribute": contribute}
        return render(request, 'QAsubmission/dasboard.html', data)
    else:
        return render(request, 'login.html')
def checkContribute(request, id):
    if request.user.is_authenticated:
        contribute = Contribution.objects.filter(TermID = id)
        response = HttpResponse()
        if(len(contribute) > 0):
            response.writelines('Yes')
            return response
        response.writelines('No')
        return response
    else:
        return render(request, 'login.html')
def comment(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        comment = request.POST.get('comment', '')
        incognito = request.POST.get('incognito', '')
        if(incognito == "incognito"):
            incognito = True
        else:
            incognito = False
        contribute = Contribution.objects.get(id=id)
        Comment.objects.create(
            UserID=request.user, ContributeID=contribute, Comment=comment, Incognito=incognito)
        return redirect('/QAManager/detail_submission/'+str(id)+"/")
    else:
        return render(request, 'login.html')
def FilterDasboard(request, year):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        faculty = Faculty.objects.all()
        dasboard = []
        for i in faculty:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM staff_contribution INNER JOIN staff_user ON staff_contribution.UserID_id = staff_user.id INNER JOIN staff_faculty ON staff_user.Faculty_id = staff_faculty.id WHERE staff_faculty.Name = '" + i.Name + "' AND staff_contribution.Create_at > '" + str(year) + "-01-1' AND staff_contribution.Create_at < '" + str(year+1)+"-01-1'")
                auth_group = cursor.fetchall()
            dasboard.append([i.Name, len(auth_group)])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT staff_faculty.Name, staff_user.id FROM staff_contribution INNER JOIN staff_user ON staff_contribution.UserID_id = staff_user.id INNER JOIN staff_faculty ON staff_user.Faculty_id = staff_faculty.id")
            contribute = cursor.fetchall()
        data = {"dasboard": dasboard, "contribute": contribute}
        return render(request, 'QAsubmission/dasboard.html', data)
    else:
        return render(request, 'login.html')


def Contributiondepartment(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        return render(request, 'index/index.html')
    else:
        return render(request, 'login.html')


def MostPopular(request, page):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contributes = Contribution.objects.all().order_by(
            "-Total_likes")[5*page-5:5*page-1]
        lenCons = len(contributes)
        Contributes = {'contribute': contributes, 'numberPage': int(lenCons/5)}
        return render(request, 'QAsubmission/all_submission.html', Contributes)
    else:
        return render(request, 'login.html')


def Latest(request, page):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contributes = Contribution.objects.all().order_by(
            "-Create_at")[5*page-5:5*page-1]
        lenCons = len(contributes)
        Contributes = {'contribute': contributes, 'numberPage': int(lenCons/5)}
        return render(request, 'QAsubmission/all_submission.html', Contributes)
    else:
        return render(request, 'login.html')

def Terms(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        term = Term.objects.all()
        data = {"term": term}
        return render(request, 'manage_term/term.html', data)
    return render(request, 'login.html')
def DetailTerm(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        term = Term.objects.get(id = id)
        data = {"term": term}
        return render(request, 'manage_term/update.html', data)
    return render(request, 'login.html')
def UpdateTerm(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        name = request.POST.get('Name', '')
        closureDate = request.POST.get('closureDate', '')
        finalClosureDate = request.POST.get('finalClosureDate', '')
        description = request.POST.get('description', '')
        print(finalClosureDate)
        term = Term.objects.get(id = id)
        term.Name = name
        term.Closure_date = closureDate
        term.Final_Closure_date = finalClosureDate
        term.Description = description
        term.save()
        return redirect('/QAManager/detailTerm/'+str(id))
    return render(request, 'login.html')
def DeleteTerm(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        Term.objects.get(id = id).delete()
        return redirect('/QAManager/terms')
    return render(request, 'login.html')
def AddTerm(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        return render(request, 'manage_term/add.html')
    return render(request, 'login.html')
def InsertTerm(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        name = request.POST.get('Name', '')
        closureDate = request.POST.get('closureDate', '')
        finalClosureDate = request.POST.get('finalClosureDate', '')
        description = request.POST.get('description', '')

        Term.objects.create(Name = name, Closure_date = closureDate, Final_Closure_date = finalClosureDate, Description = description)
        return redirect('/QAManager/terms')
    return render(request, 'login.html')

def TypeContribute(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        typeContribute = Type.objects.all()
        data = {"typeContribute": typeContribute}
        return render(request, 'manage_type/type.html', data)
    return render(request, 'login.html')
def AddType(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        return render(request, 'manage_type/add.html')
    return render(request, 'login.html')
def DeleteType(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        Type.objects.get(id = id).delete()
        return redirect('/QAManager/type')
    return render(request, 'login.html')


def UpdateType(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        name = request.POST.get('Name', '')
        description = request.POST.get('Description', '')
        typeContribute = Type.objects.get(id = id)
        typeContribute.Name = name
        typeContribute.Description = description
        typeContribute.save()
        data = {"typeContribute": typeContribute}
        return redirect('/QAManager/detailType/'+str(id))
    return render(request, 'login.html')
def Add(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        name = request.POST.get('Name', '')
        description = request.POST.get('Description', '')
        Type.objects.create(Name = name, Description = description)
        return redirect('/QAManager/type')
    return render(request, 'login.html')
def DetailType(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        typeContribute = Type.objects.get(id = id)
        data = {"typeContribute": typeContribute}
        return render(request, 'manage_type/update.html', data)
    return render(request, 'login.html')
def submission(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contribute = Contribution.objects.all()[0:4]
        typeC = Type.objects.all()
        data = {"contribute": contribute, "numberPage": len(
            contribute)/5, "typeC": typeC}
        return render(request, 'QAsubmission/all_submission.html', data)
    return render(request, 'login.html')


def submissionPage(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contribute = Contribution.objects.all()[id*5-5:id*5-1]
        typeC = Type.objects.all()
        data = {"contribute": contribute,
                "numberPage": len(contribute), "typeC": typeC}
        return render(request, 'QAsubmission/all_submission.html', data)
    return render(request, 'login.html')


def filter(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contribute = Contribution.objects.filter(TypeID=id)
        typeC = Type.objects.all()
        data = {"contribute": contribute,
                "numberPage": len(contribute), "typeC": typeC}
        return render(request, 'QAsubmission/all_submission.html', data)
    return render(request, 'login.html')


def detail_submission(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        contribution = Contribution.objects.get(id=id)
        user = request.user
        term = Term.objects.get(id=contribution.TermID)
        is_final_Closure_date = False
        if term.Final_Closure_date.date() < date.today():
            is_final_Closure_date = True
        is_Closure_date = False
        if term.Closure_date.date() < date.today():
            is_Closure_date = True
        print(is_final_Closure_date)
        comment = Comment.objects.filter(
            ContributeID=id).order_by('-Create_at')
        like = Like.objects.filter(User_ID1=user, ContributeID=id, Like=True)
        data = {"contribution": contribution, "user": user, "term": term, "comment": comment, "like": len(
            like), "is_final_Closure_date": is_final_Closure_date, "is_Closure_date": is_Closure_date}
        return render(request, 'QAsubmission/detail_submission.html', data)
    return render(request, 'login.html')


def profile(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        user = request.user
        print(user.Faculty)
        data = {"user": user}
        return render(request, 'QAuser/profile.html')
