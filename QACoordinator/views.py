
from django.db import connection, connections
from login.views import getAuthGroup
from staff.models import Contribution, Faculty, Type, Term, Comment, Like, User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date


def index(request, page):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        per = User.objects.get(id=request.user.id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT staff_contribution.Name,staff_contribution.Create_at, staff_contribution.Total_likes,staff_contribution.id FROM staff_contribution INNER JOIN staff_user ON staff_user.id = staff_contribution.UserID_id INNER JOIN staff_faculty ON staff_faculty.id = staff_user.Faculty_id WHERE staff_faculty.id = %s", [
                    per.Faculty.id]
            )
            contributes = cursor.fetchall()
            cursor.close()
 
        lenCons = float(len(contributes)/5)
        if lenCons == int(len(contributes)/5):
            lenCons = int(len(contributes)/5)
        else:
            lenCons = int(len(contributes)/5+1)
        contributes = contributes[5*page-5:5*page]
        Contributes = {'contributes': contributes,
                       'numberPage': int(lenCons)}
        return render(request, 'CDsubmission/all_submission.html', Contributes)
    else:
        return render(request, 'login.html')


def MostPopular(request, page):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        per = User.objects.get(id=request.user.id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT staff_contribution.Name,staff_contribution.Create_at, staff_contribution.Total_likes,staff_contribution.id FROM staff_contribution INNER JOIN staff_user ON staff_user.id = staff_contribution.UserID_id INNER JOIN staff_faculty ON staff_faculty.id = staff_user.Faculty_id WHERE staff_faculty.id = %s ORDER BY ( '-Total_likes')", [
                    per.Faculty.id]
            )
            contributes = cursor.fetchall()
            cursor.close()
        lenCons = float(len(contributes)/5)
        if lenCons == int(len(contributes)/5):
            lenCons = int(len(contributes)/5)
        else:
            lenCons = int(len(contributes)/5+1)
        contributes = contributes[5*page-5:5*page]
        Contributes = {'contributes': contributes,
                       'numberPage': int(lenCons)}
        # return JsonResponse({'lenCons': lenCons})
        return render(request, 'CDsubmission/all_submission.html', Contributes)
    else:
        return render(request, 'login.html')


def Latest(request, page):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        per = User.objects.get(id=request.user.id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT staff_contribution.Name,staff_contribution.Create_at, staff_contribution.Total_likes,staff_contribution.id FROM staff_contribution INNER JOIN staff_user ON staff_user.id = staff_contribution.UserID_id INNER JOIN staff_faculty ON staff_faculty.id = staff_user.Faculty_id WHERE staff_faculty.id = %s ORDER BY ( '-Create_at')", [
                    per.Faculty.id]
            )
            contributes = cursor.fetchall()
            cursor.close()
        lenCons = float(len(contributes)/5)
        if lenCons == int(len(contributes)/5):
            lenCons = int(len(contributes)/5)
        else:
            lenCons = int(len(contributes)/5+1)
        contributes = contributes[5*page-5:5*page]
        contributes[5*page-5:5*page - 1]
        Contributes = {'contributes': contributes,
                       'numberPage': int(lenCons)}
        return render(request, 'CDsubmission/all_submission.html', Contributes)
    else:
        return render(request, 'login.html')


def detail_submission(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
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
        return render(request, 'CDsubmission/detail_submission.html', data)
    return render(request, 'login.html')


def profile(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        user = request.user
        print(user.Faculty)
        data = {"user": user}
        return render(request, 'CDuser/profile.html')
    return render(request, 'login.html')
def comment(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        comment = request.POST.get('comment', '')
        incognito = request.POST.get('incognito', '')
        if(incognito == "incognito"):
            incognito = True
        else:
            incognito = False
        contribute = Contribution.objects.get(id=id)
        Comment.objects.create(
            UserID=request.user, ContributeID=contribute, Comment=comment, Incognito=incognito)
        return redirect('/QACoordinator/detail_submission/'+str(id)+"/")
    else:
        return render(request, 'login.html')