from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json, time

from shifts.models import Employee, Schedule, Shift, Slice, Stamp,FireStampCheck,StampCheckError,FireSP,Timekeeping
from shifts.utils import stampCheck, timeEvaluation, dateValidate,deleteRow

from django.contrib.auth.models import User
#from .models import User
# Create your views here.

def index (request):
    # Authenticated users view index.html
    if request.user.is_authenticated:
       return render(request, "shifts/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

# ---- Delete records ----------------------------------------------------------------------
@csrf_exempt
@login_required
# New employee
def delRow(request):
    try:
        # Deletting a row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        id = data.get("id", "")
        table = data.get("table", "")

        # Delete row
        deleteRow(table,id)
        
        return JsonResponse({'rCode':10, "message": "Row deleted successfully." }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)

# ---- Save new records --------------------------------------------------------------------
@csrf_exempt
@login_required
def newEmployee(request):
    try:
        # Adding a new row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        firstName = data.get("firstName", "")
        lastName = data.get("lastName", "")
        employeeId = data.get("employeeId", "")

        # Save row
        row = Employee(
            user=request.user,
            firstName=firstName,
            lastName = lastName,
            employeeId = employeeId 
        )
        row.save()

        return JsonResponse({'rCode':10, "message": "Row saved successfully." }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)

@csrf_exempt
@login_required
def newShift(request):
    try:
        # Adding a new row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        label = data.get("label", "")
        description = data.get("description", "")

        # Save row
        row = Shift(
            user=request.user,
            label=label,
            description = description
        )
        row.save()

        return JsonResponse({'rCode':10, "message": "Row saved successfully." }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)

@csrf_exempt
@login_required
def newSlice(request):
    try:
        # Adding a new row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        shiftLabel = data.get("shiftLabel", "")
        label = data.get("label", "")
        description = data.get("description", "")
        stampGroup = data.get("stampGroup", "")
        start = data.get("start", "")
        end = data.get("end", "")
        requiredTime = data.get("requiredTime", "")
        presenceCode = data.get("presenceCode", "")
        absenceCode = data.get("absenceCode", "")
        overtimeCode = data.get("overtimeCode", "")
        overtimeMin = data.get("overtimeMin", "")
        overtimeStep = data.get("overtimeStep", "")

        shifts = Shift.objects.filter(label=shiftLabel,user=request.user)

        if shifts.count()==1 :        
            # Save row
            row = Slice(
                user=request.user,
                shift=shifts[0],
                label=label,
                description = description,
                stampGroup=stampGroup,
                start = start,
                end=end,
                requiredTime = requiredTime,
                presenceCode=presenceCode,
                absenceCode = absenceCode,
                overtimeCode=overtimeCode,
                overtimeMin = overtimeMin,
                overtimeStep=overtimeStep
            )
            row.save()

            return JsonResponse({'rCode':10, "message": "Row saved successfully." }, safe=False)
        else:
            return JsonResponse({'rCode':40, "errorMsg": "Related shift doesn't exist", "eCode": 102 }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)

@csrf_exempt
@login_required
def newSchedule(request):
    try:
        # Adding a new row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        day = data.get("day", "")
        shiftLabel = data.get("shiftLabel", "")
        employeeId = data.get("employeeId", "")


        shifts = Shift.objects.filter(label=shiftLabel,user=request.user)
        employees = Employee.objects.filter(employeeId=employeeId,user=request.user)

        if shifts.count()==1 and employees.count()==1:        
            # Save row
            row = Schedule(
                user=request.user,
                day=day,
                shift=shifts[0],
                employee=employees[0]
            )
            row.save()

            return JsonResponse({'rCode':10, "message": "Row saved successfully." }, safe=False)
        else:
            return JsonResponse({'rCode':40, "errorMsg": "Related shift and/or employee doesn't exist", "eCode": 102 }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)


@csrf_exempt
@login_required
def newStamp(request):
    try:
        # Adding a new row via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 102 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get fields data
        stampGroup = data.get("stampGroup", "")
        employeeId = data.get("employeeId", "")
        stampType = data.get("stampType", "")
        timestamp = data.get("timestamp", "")

        employees = Employee.objects.filter(employeeId=employeeId,user=request.user)

        if employees.count()==1:        
            # Save row
            row = Stamp(
                user=request.user,
                employee=employees[0],
                stampGroup = stampGroup,
                stampType = stampType,
                timestamp = timestamp
            )
            row.save()

            return JsonResponse({'rCode':10, "message": "Row saved successfully." }, safe=False)
        else:
            return JsonResponse({'rCode':40, "errorMsg": "Related employee doesn't exist", "eCode": 102 }, safe=False)
    
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 101 }, safe=False)


# ---- Retrieving data views --------------------------------------------------------------------

@login_required
def employeeList(request):
    try:
        rows = Employee.objects.filter(user=request.user).order_by('employeeId')
        if rows.count() > 0:
            body = [row.serialize() for row in rows]
            # response code 10 means there are rows to be shown to user
            return JsonResponse({'rCode':10,'body':body}, safe=False)
        else:
            return JsonResponse({'rCode':11, "message": "There are no rows" }, safe=False)
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 111 }, safe=False)

@login_required
def shiftList(request):
    try:
        rows = Shift.objects.filter(user=request.user).order_by('label')
        if rows.count() > 0:
            body = [row.serialize() for row in rows]
            # response code 10 means there are rows to be shown to user
            return JsonResponse({'rCode':10,'body':body}, safe=False)
        else:
            return JsonResponse({'rCode':11, "message": "There are no rows" }, safe=False)
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 111 }, safe=False)

@login_required
def sliceList(request):
    try:
        rows = Slice.objects.filter(user=request.user).order_by('shift','label','start')
        if rows.count() > 0:
            body = [row.serialize() for row in rows]
            # response code 10 means there are rows to be shown to user
            return JsonResponse({'rCode':10,'body':body}, safe=False)
        else:
            return JsonResponse({'rCode':11, "message": "There are no rows" }, safe=False)
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 111 }, safe=False)

@login_required
def scheduleList(request):
    try:
        rows = Schedule.objects.filter(user=request.user).order_by('-day','employee__employeeId')
        if rows.count() > 0:
            body = [row.serialize() for row in rows]
            # response code 10 means there are rows to be shown to user 
            return JsonResponse({'rCode':10,'body':body}, safe=False)
        else:
            return JsonResponse({'rCode':11, "message": "There are no rows" }, safe=False)
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 111 }, safe=False)

login_required
def stampList(request):
    try:
        rows = Stamp.objects.filter(user=request.user).order_by('stampGroup','employee__employeeId','timestamp')
        if rows.count() > 0:
            body = [row.serialize() for row in rows]
            # response code 10 means there are rows to be shown to user 
            return JsonResponse({'rCode':10,'body':body}, safe=False)
        else:
            return JsonResponse({'rCode':11, "message": "There are no rows" }, safe=False)
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 111 }, safe=False)

# ----Upload/Evaluation --------------------------------------------------------------------

@csrf_exempt
@login_required
def uploadStamps(request):
    try:
        # Reciving daily information via POST
        if request.method != "POST":
            return JsonResponse({'rCode':40, "errorMsg": "POST request required.", "eCode": 43 }, safe=False)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get contents 
        stamps = data.get("stamps","")
    
        # Delete all previous user's stamps
        Stamp.objects.filter(user=request.user).delete()
        
        # Save all recived stamps
        for stamp in stamps:
            stampModel = Stamp()
            if stamp['employeeId'] !='':
                employee = Employee.objects.filter(user=request.user,employeeId=stamp['employeeId'])
                if employee.count()==1:
                    stampModel.user=request.user
                    stampModel.employee = employee[0]
                    stampModel.timestamp = stamp['timestamp']
                    stampModel.stampType = stamp['stampType']
                    stampModel.stampGroup = stamp['stampGroup']
                    stampModel.save()

         # response code 10 means there are time results to be shown to user
        return JsonResponse({'rCode':10,'message':"Ok"}, safe=False)
 
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 41 }, safe=False)


@csrf_exempt
@login_required
def evaluation(request):
    try:
        # Reciving daily information via POST
        if request.method != "POST":
            return JsonResponse({"error": "POST request required."}, status=400)

        # Load request body (JS puts a Json dict in it)
        data = json.loads(request.body)

        # Get contents 
        evaluationDay = data.get("date", "")
        if not dateValidate(evaluationDay):
            return JsonResponse({'rCode':40, "errorMsg": "Evaluation date must be in YY-MM-DD format", "eCode": 42 }, safe=False)
    
        # Start stamp checking (Fire Store procedure)
        stampCheck(request.user.id,evaluationDay)
 
        # Wait and check finish process flag
        sleepFlag = True
        sleepCount = 0
        while sleepFlag:
            time.sleep(1)
            sleepCount = sleepCount + 1
            stampCheckStatus = FireStampCheck.objects.filter(user=request.user.id)
            if stampCheckStatus.count() == 1:
                if stampCheckStatus[0].status == True:
                    # Are there error rows?
                    stampErrors = StampCheckError.objects.filter(user=request.user.id).order_by('employee','timestamp')
                    if stampErrors.count() > 0:
                        # Error details
                        body = [stampError.serialize() for stampError in stampErrors]
                        # response code 20 means there are stamps error to be shown to user
                        return JsonResponse({'rCode':20,'body':body}, safe=False)
                    else:    
                        sleepFlag = False
                elif sleepCount > 59:
                    return JsonResponse({'rCode':40, "errorMsg": "Stamp checking timeout", "eCode": 21 }, safe=False)
            else:
                return JsonResponse({'rCode':40, "errorMsg": "Stamp cheching Couldn't start", "eCode": 22 }, safe=False)


        # Start time evaluation (Fire Store procedure)
        timeEvaluation(request.user.id,evaluationDay)
     
        # Wait and check finish process flag
        sleepCount = 0
        while True:
            time.sleep(1)
            sleepCount = sleepCount + 1
            spStatus = FireSP.objects.filter(user=request.user.id)
            if spStatus.count() == 1:
                if spStatus[0].status == True:
                    # Are there evaluation results?
                    timekeeping = Timekeeping.objects.filter(user=request.user.id).order_by('employee','type')
                    if timekeeping.count() > 0:
                        # Return details
                        body = [row.serialize() for row in timekeeping]
                        # response code 10 means there are time results to be shown to user
                        return JsonResponse({'rCode':10,'body':body}, safe=False)
                    else:    
                        return JsonResponse({'rCode':40, "errorMsg": "No results-Empty timekeeping table", "eCode": 11 }, safe=False)
                elif sleepCount > 59:
                    return JsonResponse({'rCode':40, "errorMsg": "Time evaluation timeout", "eCode": 12 }, safe=False)
            else:
                return JsonResponse({'rCode':40, "errorMsg": "Time evaluation Couldn't start", "eCode": 13 }, safe=False)
 
    except Exception as e:
        return JsonResponse({'rCode':40, "errorMsg": str(e), "eCode": 41 }, safe=False)


# ---- Autentication --------------------------------------------------------------------
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shifts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "shifts/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shifts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shifts/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shifts/register.html")
