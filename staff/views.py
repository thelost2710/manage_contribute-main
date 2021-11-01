from staff.models import Term
from django.shortcuts import redirect, render
from django.db import connection
from .models import Term, Contribution, Document, User, Comment, Like, Type
from django.http import HttpResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from django.http import JsonResponse
from datetime import date
from zipfile import ZipFile, ZIP_DEFLATED
import os
import zipfile
from io import BytesIO
import pickle
import base64
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build


def getAuthGroup(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_group.name FROM auth_group INNER JOIN staff_user_groups ON auth_group.id = staff_user_groups.group_id INNER JOIN staff_user ON staff_user.id = staff_user_groups.user_id WHERE staff_user.id = %s", [UserID])
        auth_group = cursor.fetchone()[0]
    return auth_group


def upload(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        term = Term.objects.get(id=id)
        contribution = Contribution.objects.filter(
            UserID=request.user, TermID=id)
        is_final_Closure_date = False
        if len(contribution) == 0:
            typeC = Type.objects.all()
            if term.Closure_date.date() > date.today():
                term = Term.objects.get(id=id)
                is_final_Closure_date = True
                data = {"is_final_Closure_date": is_final_Closure_date,
                        "typeC": typeC, "term": term}
                return render(request, 'index/upload_contribute.html', data)
            term = Term.objects.get(id=id)
            data = {"term": term, "typeC": typeC}
            return render(request, 'index/upload_contribute.html', data)
        return redirect('/staff/detail_submission/'+str(contribution[0].id)+"/")
    return render(request, 'login.html')


def deleteFile(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        Contribution.objects.get(id=id).delete()
        return redirect('/Staff')
    return render(request, 'login.html')


def profile(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        user = request.user
        print(user.Faculty)
        data = {"user": user}
        return render(request, 'user/profile.html')
    return render(request, 'login.html')


def uploadFile(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        if request.method == 'POST':
            name = request.POST.get('name', '')
            incognito = request.POST.get('incognito', '')
            typec = request.POST.get('type', '')
            description = request.POST.get('description', '')
            contribute = request.FILES['contribute']
            getType = Type.objects.get(id=typec)
            if(incognito == "incognito"):
                incognito = True
            else:
                incognito = False
            term = Term.objects.get(id=id)
            Contribution.objects.create(UserID=request.user, TermID=term, Name=name,
                                        Description=description, Total_likes=1, Incognito=incognito, TypeID=getType)
            Document.objects.create(ContributeID=Contribution.objects.latest(
                'id'), Name=name, Document_detail=contribute)

            # Send email
            # per = User.objects.get(id=request.user.id)
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         "SELECT staff_user.email FROM staff_user INNER JOIN staff_user_groups ON staff_user.id = staff_user_groups.user_id INNER JOIN auth_group ON staff_user_groups.group_id = auth_group.id INNER JOIN staff_faculty ON staff_faculty.id = staff_user.Faculty_id WHERE auth_group.name = %s AND staff_faculty.id = %s",
            #         ["QACoordinator", per.Faculty.id]
            #     )
            #     Email = cursor.fetchall()
            # for i in Email:
            #     CLIENT_SECRET_FILE = './client_secret.json'
            #     API_NAME = "gmail"
            #     API_VERSION = "v1"
            #     SCOPES = ["https://mail.google.com/"]
            #     service = Create_Service(
            #         CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            #     emailMsg = "The Staff whose name is " + User.objects.get(id=request.user.id).username+" contributes a magazine to the term "+Term.objects.get(
            #         id=id).Name+".\n Please visit here to see contributions: http://127.0.0.1:8000/QACoordinator/detail_submission/" + str(Contribution.objects.latest('id').id)+"/"
            #     mimeMessage = MIMEMultipart()
            #     mimeMessage["to"] = i[0]
            #     mimeMessage["subject"] = "Notification"
            #     mimeMessage.attach(MIMEText(emailMsg, 'plain'))
            #     raw_string = base64.urlsafe_b64encode(
            #         mimeMessage.as_bytes()).decode()
            #     message = service.users().messages().send(
            #         userId="me", body={"raw": raw_string}).execute()

            return redirect('/Staff')
    else:
        return render(request, 'login.html')


def UpdateFile(request, id, id1):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        if request.method == 'POST':
            typec = request.POST.get('type', '')
            name = request.POST.get('name', '')
            incognito = request.POST.get('incognito', '')
            description = request.POST.get('description', '')
            contribute = request.FILES['contribute']
            getType = Type.objects.get(id=typec)
            if(incognito == "incognito"):
                incognito = True
            else:
                incognito = False
            Document.objects.filter(ContributeID=id1).delete()
            Contribution.objects.filter(id=id1).delete()
            term = Term.objects.get(id=id)
            Contribution.objects.create(UserID=request.user, TermID=term, Name=name,
                                        Description=description, Total_likes=1, Incognito=incognito, TypeID=getType)
            Document.objects.create(ContributeID=Contribution.objects.latest(
                'id'), Name=name, Document_detail=contribute)
            return redirect('/Staff')
    else:
        return render(request, 'login.html')


def downloadZip(request, id):
    if request.user.is_authenticated:
        document = Document.objects.filter(ContributeID=id)
        if len(document) > 0:
            filelist = ["./media/"+str(document[0].Document_detail)]
            byte_data = BytesIO()
            zip_file = zipfile.ZipFile(byte_data, "w")
            for file in filelist:
                filename = os.path.basename(os.path.normpath(file))
                print(filename)
                zip_file.write(file, filename)
            zip_file.close()
            response = HttpResponse(
                byte_data.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=files.zip'
            response['Content-Disposition'] = 'attachment; filename=' + \
                str(Contribution.objects.get(id=id).Name)+'.zip'
            byte_data.close()
            return response
        return redirect('/Staff')
    else:
        return render(request, 'login.html')


def submission(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        contribute = Contribution.objects.all()[0:5]
        contributePage = Contribution.objects.all()
        typeC = Type.objects.all()
        page = float(len(contributePage)/5)
        if page == int(len(contributePage)/5):
            page = int(len(contributePage)/5)
        else:
            page = int(len(contributePage)/5+1)
        print(page)
        data = {"contribute": contribute, "numberPage": page, "typeC": typeC}
        return render(request, 'submission/all_submission.html', data)
    else:
        return render(request, 'login.html')


def submissionPage(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        contribute = Contribution.objects.all()[id*5-5:id*5]
        allContribute = Contribution.objects.all()
        typeC = Type.objects.all()
        data = {"contribute": contribute,
                "numberPage": int(len(allContribute)/5+1), "typeC": typeC}
        return render(request, 'submission/all_submission.html', data)
    else:
        return render(request, 'login.html')


def filter(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        contribute = Contribution.objects.filter(TypeID=id)
        typeC = Type.objects.all()
        data = {"contribute": contribute,
                "numberPage": len(contribute), "typeC": typeC}
        return render(request, 'submission/all_submission.html', data)
    else:
        return render(request, 'login.html')


def editFile(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        contribution = Contribution.objects.get(id=id)
        user = request.user
        term = Term.objects.get(id=contribution.TermID)
        is_final_Closure_date = False
        if term.Final_Closure_date.date() > date.today():
            is_final_Closure_date = True
        comment = Comment.objects.filter(
            ContributeID=id).order_by('-Create_at')
        like = Like.objects.filter(User_ID1=user, ContributeID=id, Like=True)
        typeC = Type.objects.all()
        data = {"contribution": contribution, "user": user, "term": term, "comment": comment,
                "like": len(like), "is_final_Closure_date": is_final_Closure_date, "typeC": typeC}
        return render(request, 'submission/update_contribute.html', data)
    else:
        return render(request, 'login.html')


def detail_submission(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        contribution = Contribution.objects.get(id=id)
        user = request.user
        term = Term.objects.get(id=contribution.TermID)
        is_final_Closure_date = False
        if term.Final_Closure_date.date() > date.today():
            is_final_Closure_date = True
        comment = Comment.objects.filter(
            ContributeID=id).order_by('-Create_at')
        like = Like.objects.filter(User_ID1=user, ContributeID=id, Like=True)
        data = {"contribution": contribution, "user": user, "term": term, "comment": comment,
                "like": len(like), "is_final_Closure_date": is_final_Closure_date}
        return render(request, 'submission/detail_submission.html', data)
    else:
        return render(request, 'login.html')


def like(request, id):
    if request.user.is_authenticated:
        user = request.user
        contribution = Contribution.objects.get(id=id)
        like = Like.objects.filter(User_ID1=user, ContributeID=contribution)
        if len(like) == 0:
            Like.objects.create(
                User_ID1=user, ContributeID=contribution, Like=True)
        else:
            Like.objects.filter(
                User_ID1=user, ContributeID=contribution).update(Like=True)
        contribution.Total_likes = contribution.Total_likes + 1
        contribution.save()
        return JsonResponse({'results': 'like'})
    else:
        return render(request, 'login.html')


def unLike(request, id):
    if request.user.is_authenticated:
        user = request.user
        contribution = Contribution.objects.get(id=id)
        like = Like.objects.filter(User_ID1=user, ContributeID=contribution)
        if len(like) == 0:
            Like.objects.create(
                User_ID1=user, ContributeID=contribution, Like=False)
        else:
            Like.objects.filter(
                User_ID1=user, ContributeID=contribution).update(Like=False)
        contribution.Total_likes = contribution.Total_likes - 1
        contribution.save()
        return JsonResponse({'results': 'unLike'})
    else:
        return render(request, 'login.html')


def comment(request, id):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        comment = request.POST.get('comment', '')
        incognito = request.POST.get('incognito', '')
        if(incognito == "incognito"):
            incognito = True
        else:
            incognito = False
        contribute = Contribution.objects.get(id=id)
        Comment.objects.create(
            UserID=request.user, ContributeID=contribute, Comment=comment, Incognito=incognito)
        return redirect('/staff/detail_submission/'+str(id)+"/")
    else:
        return render(request, 'login.html')


def index(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        # them order_by
        term = Term.objects.all()
        contribute = Contribution.objects.filter(UserID = request.user)
        ViewTerms = {'Term': term, "contribute": contribute}
        return render(request, 'index/index.html', ViewTerms)
    else:
        return render(request, 'login.html')


# def ViewAllContributions(request):
#     if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
#         contributes = Contribution.objects.all()
#         Contributes = {'contributes': contributes}
#         return render(request, 'AllContribute.html', Contributes)
#     else:
#         return render(request, 'login.html')


def ViewClosureDate(request):
    if request.user.is_authenticated and getAuthGroup(request.user.id) == "Staff":
        return render(request, 'ViewDeadline.html')
    else:
        return render(request, 'login.html')


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print("Unable to connect!")
        print(e)
        return None

