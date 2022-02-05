# Final project - Timekeeping

This web application was developed to process the entry and exit records from company personnel in a simple but powerful way. As a result, a list of time amounts with special attributes are given back,according to each shift settings.

## Project content 📋

This project content a Django project called 'Timekeemping' and it has a single app called 'Shifts'. The following list shows created files and their descriptions. 

* **shifts.js**: Javascript code. It allows app to be able to run many frontend functionalities, like show/hide views, handle events, ets .

* **styles.css**: Css code.

* **login.html**: Html page. It allows users to login.

* **register.html**:  Html page. It allows users to register.

* **index.html**:  Html page. It contains all frontend views.

* **utils .py**:  Python file. It contains some useful functions like firing stored procedure functions and date validation function.

* **fooStamps.txt**: cvs file. It contains some clock timestamps to testing porposes. These stamps are related to user foo's employees and can be uploaded.


## Distinctiveness and Complexity 🚀

This application is different from the ones developed in this course. It's not a social network or a commerce site, but a web app to process employee information, and provide a list of classified amount of times to be used in the salary payment system. Regarding complexity, this project has **five main Django models plus seven auxiliary models** for data processing. The main process, (time evaluation), is carried out through a **stored procedure/trigger** in the sqlite database.

Django ORM: Certain querys in the Django could be hard to make, for example _SELECT (A1.Field1 * A2.Field1 + B.Field2) AS Annotate1 FROM TableA as A1, TableA as A2, TableB as B_. ( Flexible selection of fields even with a table and itself). That is the reason for chosing a stored procedure. In addition, counting on previous experience in SQL allows to develop faster.

The app backend implements an API for all required functionalities. Users are able to require information, save new records and delete them from frontend through javascrip fetch. The entire frontend was developed in a single html file (index.html), showing and hiding the corresponding view.

## Description of the models 📋

* **Employee**: List of company employees. The employeeId field is the most important field.

* **Stamp**: List of employee's check-in and check-out records. Only two kind of stamps are valid: _IN_ for entry stamps and _OU_ for leaving stamps. This table add a _stampGroup_ field, that allows user to separate stamps by groups. For example:  building entrances stamps, dinning room stamps, etc.

* **Shift**: List of different daily work shifts of the company.

* **Schedule**: Relationship between each employee and their corresponding shift on a specific date. For example, employee Id = 1000 is assigned to shift 2WD on 2021-9-01.

* **Slice**: It's the most important table, where time segment attributes are defined. Each shift could have many slices. Each slice is a time catcher, as you can see in the following example:

_The time span: 72 hours. Previous day - process day - next day. The system works based in minutes so, the range goes from 0 to 4319. (it means from previous day at 00:00 to next day at 23:59).This allows flexible shifts, starting the day before, or ending the day after_

```
Example: Employee entered at 7:00 and left at 15:00 on the process day (from 1860 to 2340). If there is a slice that "catches" times from 2000 to 2500, then process will generate a record contains an amount of 2340-2000 = 340 minutes clasified according slice attributes.
```

Each logged in user can access the models data through settings menu. It's important to know that each table has the "user" field, which allows simultaneous processing of many users.

## Slice model - main fields (Catcher attributes) ⚙️

* **stampGroup**: The group of stamps this slice is catching for:

* **start and end**: The beginning and the end of slice. (Minutes between 0 to 4319):

* **requiredTime**: This field indicates the mandatory working time within the slice.
    * requiredTime = 0 : There is no required time. All time inside this slice will be consider overtime "O"
    
    * requiredTime = end-start :The whole slice is considered required. This means this slice is a FIXED mandatory slice. All time inside this slice will be consider presence "P". If required time were not completed by employee, missing time would be consider absence "A"

    * requiredTime > 0 but < end-start : This means that this slice is a FLEXIBLE mandatory slice. All time inside this slice UP TO _requided_, will be consider presence "P". If required time were not completed, missing time would be consider absence "A". If required time were exceeded, it will be consider overtime "O"    

* **presenceCode**: Attribute to be assigned to presences.
* **absenceCode**: Attribute to be assigned to absences.
* **overtimeCode**: Attribute to be assigned to overtime.
* **overtimeMin**: Minimum threshold to consider overtime.
* **overtimeStep**: Minimum fraction of overtime.

    _Overtime example: Min 30 minutes, Step 15 minutes._

    ``` 
    Overtime = overtimeMin + n * overtimeStep
    If an employee works 73 minutes beyond the required time it will result: 30 + 2*15 = 60 minutes.
    If an employee works 79 minutes beyond the required time it will result: 30 + 3*15 = 75 minutes.
    ```


## Test environment ⚙️

### Run application 
_It can be started just as allways:_

```
 python manage.py runserver 
```

### Registred Users ⌨️

_There are two users for different purposes._

```
foo: Password: 1234: Full test environment 🚀: 5 employees have been assigned to 5 different shifts. Each shift has many slices to capture time lapses and classify them. All those attributes can be seen in settings->slices. There is a set of clock's timestamp for every employee in order to generate diferent situations (presences, absences, overtime, fixed shifts, flexible shifts).Testers are able to evaluate and see resulting outputs. 

bar: Password: 1234: Sandbox 📦: Just one employee. Just one shift. This shift has only one slice to capture time lapses and classify them. There is a couple of clock's timestamp. Testers are able to change one or more slice's fields and evaluate to see resulting outputs. The same is valid to timestamps in order to see results for diferent scenarios. 

```
### Run time-evaluation 🖇️

_This section explain how to see, upload and modify timestamps and how to check and evatuate them. All these functionalities can be done going to System->Time Evaluation_

* Clock stamps 📌: Once users enter in System->Time Evaluation, they can see all their timestamps. As all tables in the system, it's possible to add new records and/or delete them. Users are able to upload timestamp instead of add one by one, clicking on 'choose file' button. There is a file called fooStamps.txt for this purpose. This file is a cvs file containing clock stamps for user foo's  employees. If a upload is perform, all existing timestams will be deleted. The upload is performed in javascript splitting each row in file, using _contents.split("\r\n")_ in line 638. This runs properly in windows, but it's possible this has to be changed in mac or other operating systems.

* Time evaluation 🛠️: If **foo** user is logged in, he will be able to click on 'Time evaluation' button and then, enter 2021-09-17 in the popup message as evaluation day. After few seconds, a table with results will appear. There is an employee (id=2155) who has continued working to the next day, so it's possible to evaluate that day (2021-09-18) and see the results. The same is valid for **bar** user, but entering 2021-09-01 in the popup message as evaluation day. 






* Clock stamps check 📢: Before running time evaluation, the system runs a process to check stamp inconsistences.If two stamps have the same type (Two *IN* or two *OU* together) in chronological order, it will show an inconsistence. Testers are able to force inconsistences: 

    ```
       Suggestion: delete following foo records 
       
       empid = 4443	OU	2021-09-17 11:05:00
       empId = 4444	IN	2021-09-17 13:44:00
    ```
    If user click on 'Time Evaluation' again for 2021-09-17, it will appear a table with all inconsistences detected. User is able to fix that issues by deleting and/or adding timestamps.


## Author ✒️

* **Pedro Jorge Pavón**  - [jorgepavon](https://www.linkedin.com/in/jorgepavon/)


