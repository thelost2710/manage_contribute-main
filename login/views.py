from django.db import connection
from django.shortcuts import redirect, render
from staff.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout


def getAuthGroup(UserID):
    isAdmin = User.objects.filter(id=UserID, is_superuser=True)
    if(len(isAdmin) != 0):
        return redirect('/logout')
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT auth_group.name FROM auth_group INNER JOIN staff_user_groups ON auth_group.id = staff_user_groups.group_id INNER JOIN staff_user ON staff_user.id = staff_user_groups.user_id WHERE staff_user.id = %s", [UserID])
            auth_group = cursor.fetchall()[0][0]
        return auth_group


def login(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        return redirect('/staff/')
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
        return redirect('/QAManager/')
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
        return redirect('/QACoordinator/1/')
    else:
        return render(request, 'login.html')


def forgotPassword(request):
    return render(request, 'forgotPassword.html')


def indexUser(request):
    if request.method == 'POST':
        userName = request.POST.get('username', '')
        passWord = request.POST.get('password', '')
        user = authenticate(username=userName, password=passWord)
        if(user is not None):
            userID = User.objects.filter(username=userName)[0].id
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT auth_group.name FROM auth_group INNER JOIN staff_user_groups ON auth_group.id = staff_user_groups.group_id INNER JOIN staff_user ON staff_user.id = staff_user_groups.user_id WHERE staff_user.id = %s", [userID])
                auth_group = cursor.fetchall()[0][0]
            request.session.set_expiry(86400)
            auth_login(request, user)
            if(auth_group == "Staff"):
                return redirect('/Staff')
            elif (auth_group == "QAManager"):
                return redirect('/QAManager/')
            elif (auth_group == "QACoordinator"):
                return redirect('/QACoordinator/1/')
            return render(request, 'login.html')
        else:
            error = {
                'error': 'Username or password is incorrect, please try again!'}
            return render(request, 'login.html', error)
    else:
        if request.user.is_authenticated:
            if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
                return render(request, 'staff/index/index.html')
            if request.user.is_authenticated and getAuthGroup(request.user.id) == "QAManager":
                return redirect('/QAManager/')
            if request.user.is_authenticated and getAuthGroup(request.user.id) == "QACoordinator":
                return redirect('/QACoordinator/')
        else:
            return render(request, 'login.html')


def logout(request):
    django_logout(request)
    return render(request, 'login.html')
