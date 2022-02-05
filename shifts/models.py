from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import Max,Sum,Count, constraints
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, related_name='user_employees', db_constraint=True)    
    firstName = models.CharField(max_length=20, null=False)
    lastName = models.CharField(max_length=20, null=False)
    employeeId = models.IntegerField(null=False)
    schedules = models.ManyToManyField('Shift', through='Schedule',
                                           symmetrical=False,
                                           related_name='employees_asigned')
    class Meta:
        constraints =(
            UniqueConstraint(fields=['user', 'employeeId'], name='uniqueEmployeeId'), 
        )

    def serialize(self):        
        return {
            "id":self.id,
            "firstName": self.firstName, 
            "lastName": self.lastName,
            "employeeId": self.employeeId
        }

    def __str__(self):
        return f"{self.user.username}: Customized Id: {self.employeeId} Last name: {self.firstName}"


class Stamp(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, related_name='user_stamps')
    employee = models.ForeignKey(Employee,on_delete=CASCADE, related_name='employee_stamps')
    stampGroup = models.CharField(max_length=3,null=False )    
    stampType = models.CharField(max_length=2,null=False)
    timestamp=models.DateTimeField(null=False)
    
    class Meta:
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(stampType='IN') | Q(stampType='OU'),
                name='stampType_MustBe_IN_or_OU'),  
            UniqueConstraint(fields=['user', 'employee','timestamp'], name='duplicateTimestamp'), 
        )

    def serialize(self):        
        return {
            "id":self.id,
            "stampGroup": self.stampGroup,
            "employeeId": self.employee.employeeId,
            "stampType": self.stampType,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"{self.user.username}: {self.employee.employeeId} - {self.employee.firstName} Stamp: {self.timestamp}"


class Shift(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, related_name='user_shifts')
    label = models.CharField(max_length=20,null=False)
    description = models.CharField(max_length=128,null=False)

    class Meta:
        constraints =(
            UniqueConstraint(fields=['user', 'label'], name='uniqueShiftlabel'), 
        )
    
    def serialize(self):        
        return {
            "id":self.id,
            "label": self.label, 
            "description": self.description
        }

    def __str__(self):
        return f"Shift: {self.label}"


class Slice(models.Model):    
    user = models.ForeignKey(User,on_delete=CASCADE, related_name='user_slices')
    shift = models.ForeignKey(Shift,on_delete=CASCADE, related_name='slices')
    label = models.CharField(max_length=20,null=False)
    description  = models.CharField(max_length=64,null=False)
    stampGroup = models.CharField(max_length=3,null=False)
    start = models.IntegerField(null=False)
    end = models.IntegerField(null=False)
    requiredTime = models.IntegerField(null=False)
    presenceCode = models.CharField(max_length=3,null=False)
    absenceCode = models.CharField(max_length=3,null=False)
    overtimeCode = models.CharField(max_length=3,null=False)
    overtimeMin = models.IntegerField(null=False)
    overtimeStep = models.IntegerField(null=False)    

    class Meta:
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(start__gte=0) & Q(start__lte=4320),
                name='start_range'),
            
            CheckConstraint(
                check=Q(end__gte=0) & Q(end__lte=4320),
                name='end_range'),
            
            CheckConstraint(
                check=Q(start__lte=models.F('end')),
                name='start_end_lessthan'),    
            
            CheckConstraint(
                check=Q(requiredTime__lte=(models.F('end')-models.F('start'))),
                name='requiredTime_lessthan'),    
        )

    def serialize(self):        
        return {
            "id":self.id,
            "shiftLabel": self.shift.label, 
            "label": self.label, 
            "description": self.description,
            "stampGroup": self.stampGroup, 
            "start": self.start, 
            "end": self.end,
            "requiredTime": self.requiredTime, 
            "presenceCode": self.presenceCode, 
            "absenceCode": self.absenceCode,
            "overtimeCode": self.overtimeCode, 
            "overtimeMin": self.overtimeMin, 
            "overtimeStep": self.overtimeStep
        }

    def __str__(self):
        return f"{self.shift} from {self.start} to {self.end}"

        

class Schedule(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, related_name='user_schedules') 
    employee =  models.ForeignKey(Employee,on_delete=CASCADE, related_name='employee_schedules')
    shift = models.ForeignKey(Shift,on_delete=CASCADE, related_name='shift_schedules') 
    day = models.DateField(null=False)
    
    def serialize(self):        
        return {
            "id":self.id,
            "day": self.day,
            "shiftLabel": self.shift.label,
            "employeeId": self.employee.employeeId 

        }
    class Meta:
        constraints =(
            UniqueConstraint(fields=['user', 'employee','day'], name='uniqueDay'), 
        )
    
    def __str__(self):
        return f"{self.day}: {self.employee.lastName} ({self.employee.employeeId}) -> {self.shift.label} shift"


# Auxiliary Tables/Models
#----------------------------------------------------------------------------------------------------------------------------

# Every row inserted in this table, will fire a trigger that will execute the Stamps checking for a specific user and date.
# For each stamp, this procedure will look for a next one in chronological order. If the next stamp has the same type... 
# IN=IN or OU=OU, an error is detected: IN=In means a OU stamp is missing or IN stamp is left over, and OU=OU means a IN stamp is missing,
# or OU stamp is left over. This runs as a store procedure, in which user and date fields act as parameters.
class FireStampCheck(models.Model):
    user = models.IntegerField(null=False)
    day = models.DateField(null=False)
    status = models.BooleanField(null=False)

# If errors are detected, they will be saved in this table
class StampCheckError(models.Model):
    user = models.IntegerField(null=False)
    employee = models.IntegerField(null=False)
    day = models.DateField(null=False)
    stampType = models.CharField(max_length=2,null=False)
    timestamp=models.DateTimeField()
    errorMessage = models.CharField(max_length=32,null=False)
 
    def serialize(self):
        employeeRow = Employee.objects.filter(id=self.employee)[0]
        return {
            "employeeId": employeeRow.employeeId, 
            "day": self.day,
            "stampType": self.stampType,
            "timestamp": self.timestamp,
            "errorMessage": self.errorMessage
        }

# Every row inserted in this table, will fire a trigger that will execute the time evaluation for a particular user and date.
# This runs as a store procedure, in which user and date fields act as parameters.
class FireSP(models.Model):
    user = models.IntegerField(null=False)
    day = models.DateField(null=False)
    status = models.BooleanField(null=False)

# In the begining, stamps come one by one in each row. It's needed to make 'Time-pairs' whith them.
# Once time-pairs are made, timestamps are converted to minutes, according to evaluation day and 'the 72 hours span'  (previous day-evaluation day- next day)
# 'Time-pairs' are stored in this table for further actions.
class Pair(models.Model):
    user = models.IntegerField(null=False)
    employee = models.IntegerField(null=False)
    stampGroup = models.CharField(max_length=3,null=False)
    day = models.DateField(null=False)
    entry = models.DateField(null=False)
    exit = models.DateField(null=False)
    entryMin = models.IntegerField(null=False)
    exitMin = models.IntegerField(null=False)

# The result of raw matching between 'Time-pairs' and Shifts slices, is stored in this table as a balance of time for each match
class Balance(models.Model):
    user = models.IntegerField(null=False)
    employee = models.IntegerField(null=False)
    day = models.DateField(null=False)
    slice = models.IntegerField(null=False)
    start = models.IntegerField(null=False)
    end = models.IntegerField(null=False)
    balance = models.IntegerField(null=False)

# Balance table agrouped by shift slice. Any employee is able to be present in more than one period of time in the same shift slice
class BalanceGroup(models.Model):
    user = models.IntegerField(null=False)
    employee = models.IntegerField(null=False)
    day = models.DateField(null=False)
    slice = models.IntegerField(null=False)
    balance = models.IntegerField(null=False)

# The final table, containing all amounts of time, clasified by Presence, Absence or Overtime with corespondig codes
class Timekeeping(models.Model):
    user = models.IntegerField(null=False)
    employee = models.IntegerField(null=False)
    day = models.DateField(null=False)
    type = models.CharField(max_length=3,null=False)
    code = models.CharField(max_length=3,null=False)
    amount = models.IntegerField(null=False)

    def serialize(self):
        employeeRow = Employee.objects.filter(id=self.employee)[0]
        return {
            "employeeId": employeeRow.employeeId,
            "day": self.day,
            "type": self.type,
            "code": self.code,
            "amount": self.amount
            
        }