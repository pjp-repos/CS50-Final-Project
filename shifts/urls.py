from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    
    # Execute upload stamps process
    path('uploadstamps', views.uploadStamps, name = 'uploadStamps'),
    # Execute Time evaluation process
    path('evaluation', views.evaluation, name = 'evaluation'),    

    #CRUDs

    # Create a new rows
    path("newemployee", views.newEmployee, name="newEmployee"),
    path("newshift", views.newShift, name="newShift"),
    path("newslice", views.newSlice, name="newSlice"),
    path("newschedule", views.newSchedule, name="newSchedule"),
    path("newstamp", views.newStamp, name="newStamp"),

    # Recordsets
    path("employeelist", views.employeeList, name="employeeList"),
    path("shiftlist", views.shiftList, name="shiftList"),
    path("slicelist", views.sliceList, name="sliceList"),
    path("schedulelist", views.scheduleList, name="scheduleList"),
    path("stamplist", views.stampList, name="stampList"),
    
    # Delete rows
    path("delrow", views.delRow, name="employeeList"),
]
