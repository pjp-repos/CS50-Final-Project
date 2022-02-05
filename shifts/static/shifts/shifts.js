// Event listeners
document.addEventListener('DOMContentLoaded',() =>{  
    
    document.getElementById('input-uploadStamp').addEventListener('change', readSingleFile, false);
    document.getElementById('btn-evaluation').addEventListener('click', timeEvaluation, false);
    
    // Menu events
    document.getElementById('menu-Employees').addEventListener('click', view_EmployeeList, false);
    document.getElementById('menu-Shifts').addEventListener('click', view_ShiftList, false);
    document.getElementById('menu-Slices').addEventListener('click', view_SliceList, false);
    document.getElementById('menu-Schedule').addEventListener('click', view_ScheduleList, false);
    document.getElementById('menu-Evaluation').addEventListener('click', view_StampList, false);
    document.getElementById('menu-Help').addEventListener('click', testMenuEvent, false);

    // form submit button events
    document.getElementById('btn-SubmitNewEmployee').addEventListener('click', newEmployee, false);
    document.getElementById('btn-SubmitNewShift').addEventListener('click', newShift, false);
    document.getElementById('btn-SubmitNewSlice').addEventListener('click', newSlice, false);
    document.getElementById('btn-SubmitNewSchedule').addEventListener('click', newSchedule, false);
    document.getElementById('btn-SubmitNewStamp').addEventListener('click', newStamp, false);

    // Events for New buttons on lists
    document.querySelector('#btn-NewEmployee').addEventListener('click', () => showView("NewEmployee"));
    document.querySelector('#btn-NewShift').addEventListener('click', () => showView("NewShift"));
    document.querySelector('#btn-NewSlice').addEventListener('click', () => showView("NewSlice"));
    document.querySelector('#btn-NewSchedule').addEventListener('click', () => showView("NewSchedule"));
    document.querySelector('#btn-NewStamp').addEventListener('click', () => showView("NewStamp"));
    
    showView('');
});

// Function for show and hide views
function showView(view){
        // Hide all views
        document.querySelector('#view-NewEmployee').style.display = 'none';
        document.querySelector('#view-EmployeeList').style.display = 'none';
        document.querySelector('#view-NewShift').style.display = 'none';
        document.querySelector('#view-ShiftList').style.display = 'none';
        document.querySelector('#view-NewSlice').style.display = 'none';
        document.querySelector('#view-SliceList').style.display = 'none';
        document.querySelector('#view-NewSchedule').style.display = 'none';
        document.querySelector('#view-ScheduleList').style.display = 'none';
        document.querySelector('#view-NewStamp').style.display = 'none';
        document.querySelector('#view-StampList').style.display = 'none';
        document.querySelector('#view-StampError').style.display = 'none';
        document.querySelector('#view-TimeResult').style.display = 'none';
        switch(view){
            case 'NewEmployee':
                document.querySelector('#view-NewEmployee').style.display = 'block';
                break;
            case 'EmployeeList':
                document.querySelector('#view-EmployeeList').style.display = 'block';
                break;
            case 'NewShift':
                document.querySelector('#view-NewShift').style.display = 'block';
                break;
            case 'ShiftList':
                document.querySelector('#view-ShiftList').style.display = 'block';
                break;
            case 'NewSlice':
                document.querySelector('#view-NewSlice').style.display = 'block';
                break;
            case 'SliceList':
                document.querySelector('#view-SliceList').style.display = 'block';
                break;
            case 'NewSchedule':
                document.querySelector('#view-NewSchedule').style.display = 'block';
                break;
            case 'ScheduleList':
                document.querySelector('#view-ScheduleList').style.display = 'block';
                break;
            case 'NewStamp':
                document.querySelector('#view-NewStamp').style.display = 'block';
                break;
            case 'StampList':
                document.querySelector('#view-StampList').style.display = 'block';
                break;
            case 'StampError':
                document.querySelector('#view-StampError').style.display = 'block';
                break;
            case 'view-TimeResult':
                document.querySelector('#view-TimeResult').style.display = 'block';
                break;

        }
};

// New row functions---------------------------------

function newEmployee(){

    // API route to save a new employee
    console.log('Fetching to save new employee... --------->')
    fetch('/newemployee', {
        method: 'POST',
        body: JSON.stringify({
            firstName : document.querySelector('#frmNeField-firstName').value,
            lastName : document.querySelector('#frmNeField-lastName').value,
            employeeId : document.querySelector('#frmNeField-employeeId').value,    
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Save new employee results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                //Clean form
                document.querySelector('#frmNeField-firstName').value="";
                document.querySelector('#frmNeField-lastName').value="";
                document.querySelector('#frmNeField-employeeId').value="";
                view_EmployeeList();
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
};

function newShift(){

    // API route to save a new shift
    console.log('Fetching to save new shift... --------->')
    fetch('/newshift', {
        method: 'POST',
        body: JSON.stringify({
            label : document.querySelector('#frmNshField-label').value,
            description : document.querySelector('#frmNshField-description').value,  
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Save new shift results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                // Clean Form
                document.querySelector('#frmNshField-label').value="";
                document.querySelector('#frmNshField-description').value="";
                view_ShiftList();
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
};

function newSlice(){

    // API route to save a new employee
    console.log('Fetching to save new slice... --------->')
    fetch('/newslice', {
        method: 'POST',
        body: JSON.stringify({
            shiftLabel : document.querySelector('#frmNslField-shiftLabel').value,
            label : document.querySelector('#frmNslField-label').value,
            description: document.querySelector('#frmNslField-description').value,    
            stampGroup : document.querySelector('#frmNslField-stampGroup').value,            
            start : document.querySelector('#frmNslField-start').value, 
            end : document.querySelector('#frmNslField-end').value,
            requiredTime : document.querySelector('#frmNslField-requiredTime').value,
            presenceCode : document.querySelector('#frmNslField-presenceCode').value,
            absenceCode : document.querySelector('#frmNslField-absenceCode').value, 
            overtimeCode : document.querySelector('#frmNslField-overtimeCode').value,
            overtimeMin : document.querySelector('#frmNslField-overtimeMin').value,
            overtimeStep : document.querySelector('#frmNslField-overtimeStep').value, 

        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Save new slice results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                //Clean form
                document.querySelector('#frmNslField-label').value="";
                document.querySelector('#frmNslField-description').value="";    
                document.querySelector('#frmNslField-stampGroup').value="";           
                document.querySelector('#frmNslField-start').value=""; 
                document.querySelector('#frmNslField-end').value="";
                document.querySelector('#frmNslField-requiredTime').value="";
                document.querySelector('#frmNslField-presenceCode').value="";
                document.querySelector('#frmNslField-absenceCode').value=""; 
                document.querySelector('#frmNslField-overtimeCode').value="";
                document.querySelector('#frmNslField-overtimeMin').value="";
                document.querySelector('#frmNslField-overtimeStep').value="";
                view_SliceList();
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
};

function newSchedule(){

    // API route to save a new employee
    console.log('Fetching to save new schedule... --------->')
    fetch('/newschedule', {
        method: 'POST',
        body: JSON.stringify({
            day : document.querySelector('#frmNscField-day').value,
            shiftLabel : document.querySelector('#frmNscField-shiftLabel').value,
            employeeId : document.querySelector('#frmNscField-employeeId').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Save new schedule results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                //Clean form
                view_ScheduleList();
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
};

function newStamp(){

    // API route to save a new employee
    console.log('Fetching to save new stamp... --------->')
    fetch('/newstamp', {
        method: 'POST',
        body: JSON.stringify({
            stampGroup : document.querySelector('#frmNstField-stampGroup').value,
            employeeId : document.querySelector('#frmNstField-employeeId').value,
            stampType : document.querySelector('#frmNstField-stampType').value,
            timestamp : document.querySelector('#frmNstField-timestamp').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Save new stamp results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                //Clean form
                view_StampList();
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
};

// DELETE function---------------------------------
function delRow(table,id){
    if(confirm("Are you sure you want to delete this record?")){
        // API route to save a new employee
        console.log(`Fetching to delete row of ${table} table... --------->`)
        fetch('/delrow', {
            method: 'POST',
            body: JSON.stringify({
                id : id,
                table: table,   
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(`<---------Result of delete row of ${table} table.`)
            console.log(result);
            switch(result.rCode){
                case 10:    // Successfull
                    switch(table){
                        case "employee":
                            view_EmployeeList();
                            break;
                        case "shift":
                            view_ShiftList();
                            break;
                        case "slice":
                            view_SliceList();
                            break;
                        case "schedule":
                            view_ScheduleList();
                            break;
                        case "stamp":
                            view_StampList();
                            break;
                    };                
                    break;   
                case 40:    // Errors
                    alert(result.errorMsg);
                    break; 
            };        
        });
    };

};

// LIST functions---------------------------------
function view_EmployeeList(){
    // Clean table body
    document.querySelector('#tbody-EmployeeList').innerHTML=""
    // Clean employee dropdowns 
    document.querySelector('#frmNscField-employeeId').innerHTML=""
    document.querySelector('#frmNstField-employeeId').innerHTML=""
    
    // API route for get list of employee
    console.log('Fetching to get list of employee... --------->')
    fetch('/employeelist')
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Get list of employee results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                result.body.forEach(row => {
                    let tr = document.createElement('tr');
                    let th = document.createElement('th');
                    let td1 = document.createElement('td');
                    let td2 = document.createElement('td');
                    let td3 = document.createElement('td');

                    // Delete button
                    let delBtn = document.createElement('button');
                    delBtn.type = "button";
                    delBtn.class = "btn btn-danger";
                    delBtn.innerHTML = `<i class="far fa-trash-alt">Delete`;
                    delBtn.onclick = () => delRow('employee',row.id);  
                       
                    // Populating fields
                    th.innerHTML = row.employeeId;
                    td1.innerHTML = row.firstName;
                    td2.innerHTML = row.lastName;
                    td3.append(delBtn); 
                    //`<button type="button" class="btn btn-danger"><i class="far fa-trash-alt">Delete</i></button>`

                    // Nesting field into row
                    tr.append(th);
                    tr.append(td1);
                    tr.append(td2);
                    tr.append(td3);

                    // Insert new row into table body
                    document.querySelector('#tbody-EmployeeList').append(tr);
                    
                    // Prepopulating dropdown box
                    let optionEmp1 = document.createElement('option');
                    let optionEmp2 = document.createElement('option');
                    optionEmp1.innerHTML = row.employeeId;
                    optionEmp2.innerHTML = row.employeeId; 
                    document.querySelector('#frmNscField-employeeId').append(optionEmp1);
                    document.querySelector('#frmNstField-employeeId').append(optionEmp2);    
                });
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
    //Show view
    showView('EmployeeList');
};

function view_ShiftList(){
    // Clean table body
    document.querySelector('#tbody-ShiftList').innerHTML=""
    // Clean shift dropdown boxes
    document.querySelector('#frmNslField-shiftLabel').innerHTML=""
    document.querySelector('#frmNscField-shiftLabel').innerHTML=""
    
    // API route for get list of shifts
    console.log('Fetching to get list of shifts... --------->')
    fetch('/shiftlist')
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Get list of shift results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                result.body.forEach(row => {
                    let tr = document.createElement('tr');
                    let th = document.createElement('th');
                    let td1 = document.createElement('td');
                    let td2 = document.createElement('td');

                    // Delete button
                    let delBtn = document.createElement('button');
                    delBtn.type = "button";
                    delBtn.class = "btn btn-danger";
                    delBtn.innerHTML = `<i class="far fa-trash-alt">Delete`;
                    delBtn.onclick = () => delRow('shift',row.id);  
                       
                    // Populating fields
                    th.innerHTML = row.label;
                    td1.innerHTML = row.description;
                    td2.append(delBtn); 

                    // Nesting field into row
                    tr.append(th);
                    tr.append(td1);
                    tr.append(td2);

                    // Insert new row into table body
                    document.querySelector('#tbody-ShiftList').append(tr);

                    // Prepopulating dropdown box
                    let option1 = document.createElement('option');
                    let option2 = document.createElement('option');
                    option1.innerHTML = row.label; 
                    option2.innerHTML = row.label;
                    document.querySelector('#frmNslField-shiftLabel').append(option1);
                    document.querySelector('#frmNscField-shiftLabel').append(option2);                   
                });
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
    //Show view
    showView('ShiftList');
};

function view_SliceList(){
    // Clean table body
    document.querySelector('#tbody-SliceList').innerHTML=""
     
    // API route for get list of slices
    console.log('Fetching to get list of slices... --------->')
    fetch('/slicelist')
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Get list of slice results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                result.body.forEach(row => {
                    let tr = document.createElement('tr');
                    let th = document.createElement('th');
                    let td1 = document.createElement('td');
                    let td2 = document.createElement('td');
                    let td3 = document.createElement('td');
                    let td4 = document.createElement('td');
                    let td5 = document.createElement('td');
                    let td6 = document.createElement('td');
                    let td7 = document.createElement('td');
                    let td8 = document.createElement('td');
                    let td9 = document.createElement('td');
                    let td10 = document.createElement('td');
                    let td11 = document.createElement('td');
                    let td12 = document.createElement('td');

                    // Delete button
                    let delBtn = document.createElement('button');
                    delBtn.type = "button";
                    delBtn.class = "btn btn-danger";
                    delBtn.innerHTML = `<i class="far fa-trash-alt">Delete`;
                    delBtn.onclick = () => delRow('slice',row.id);  
                       
                    // Populating fields
                    th.innerHTML = row.shiftLabel;
                    td1.innerHTML = row.label;
                    td2.innerHTML = row.description;
                    td3.innerHTML = row.stampGroup;
                    td4.innerHTML = row.start;
                    td5.innerHTML = row.end;
                    td6.innerHTML = row.requiredTime;
                    td7.innerHTML = row.presenceCode;
                    td8.innerHTML = row.absenceCode;
                    td9.innerHTML = row.overtimeCode;
                    td10.innerHTML = row.overtimeMin;
                    td11.innerHTML = row.overtimeStep;
                    td12.append(delBtn);

                    // Nesting field into row
                    tr.append(th);
                    tr.append(td1);
                    tr.append(td2);
                    tr.append(td3);
                    tr.append(td4);
                    tr.append(td5);
                    tr.append(td6);
                    tr.append(td7);
                    tr.append(td8);
                    tr.append(td9);
                    tr.append(td10);
                    tr.append(td11);
                    tr.append(td12);

                    // Insert new row into table body
                    document.querySelector('#tbody-SliceList').append(tr);
                });
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
    //Show view
    showView('SliceList');
};

function view_ScheduleList(){
    // Clean table body
    document.querySelector('#tbody-ScheduleList').innerHTML=""
    
    // API route for get list of slices
    console.log('Fetching to get list of schedules... --------->')
    fetch('/schedulelist')
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Get list of schedule results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                result.body.forEach(row => {
                    let tr = document.createElement('tr');
                    let th = document.createElement('th');
                    let td1 = document.createElement('td');
                    let td2 = document.createElement('td');  
                    let td3 = document.createElement('td');                   

                    // Delete button
                    let delBtn = document.createElement('button');
                    delBtn.type = "button";
                    delBtn.class = "btn btn-danger";
                    delBtn.innerHTML = `<i class="far fa-trash-alt">Delete`;
                    delBtn.onclick = () => delRow('schedule',row.id);  
                       
                    // Populating fields
                    th.innerHTML = row.day;
                    td1.innerHTML = row.employeeId;
                    td2.innerHTML = row.shiftLabel;
                    td3.append(delBtn);

                    // Nesting field into row
                    tr.append(th);
                    tr.append(td1);
                    tr.append(td2);
                    tr.append(td3);

                    // Insert new row into table body
                    document.querySelector('#tbody-ScheduleList').append(tr);
                });
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
    //Show view
    showView('ScheduleList');
};

function view_StampList(){
    // Clean table body
    document.querySelector('#tbody-StampList').innerHTML=""
    
    // API route for get list of slices
    console.log('Fetching to get list of stamps... --------->')
    fetch('/stamplist')
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log('<--------- Get list of stamp results.')
        console.log(result);
        switch(result.rCode){
            case 10:    // Successfull
                result.body.forEach(row => {
                    let tr = document.createElement('tr');
                    let th = document.createElement('th');
                    let td1 = document.createElement('td');
                    let td2 = document.createElement('td');  
                    let td3 = document.createElement('td'); 
                    let td4 = document.createElement('td');                   

                    // Delete button
                    let delBtn = document.createElement('button');
                    delBtn.type = "button";
                    delBtn.class = "btn btn-danger";
                    delBtn.innerHTML = `<i class="far fa-trash-alt">Delete`;
                    delBtn.onclick = () => delRow('stamp',row.id);  
                       
                    // Populating fields
                    th.innerHTML = row.stampGroup;
                    td1.innerHTML = row.employeeId;
                    td2.innerHTML = row.stampType;
                    td3.innerHTML = row.timestamp;
                    td4.append(delBtn);

                    // Nesting field into row
                    tr.append(th);
                    tr.append(td1);
                    tr.append(td2);
                    tr.append(td3);
                    tr.append(td4);

                    // Insert new row into table body
                    document.querySelector('#tbody-StampList').append(tr);
                });
                break;   
            case 40:    // Errors
                alert(result.errorMsg);
                break; 
        };        
    });
    //Show view
    showView('StampList');
};

function testMenuEvent(){
    alert('Please go to readme.md file!')
}

// Upload file and send stamps through API
function readSingleFile(evt) {
    try{
        //Retrieve the first (and only!) File from the FileList object
        var f = evt.target.files[0]; 

        if (f) {
            var r = new FileReader();
            r.onload = function(e) { 
                var contents = e.target.result;
                
                var lines = contents.split("\r\n");
                var line = [];
                var stamps = [];
                var output = {
                    stamps: ''
                };

                for (var i=0; i<lines.length; i++){
                    line = lines[i].split(";");
                    stamps[i] = {employeeId:line[0],timestamp:line[1],stampType:line[2],stampGroup:line[3]}
                }
                output.stamps = stamps
                
                // API route to send daily information
                console.log('Fetching to upload stamps---------> ')
                fetch('/uploadstamps', {
                    method: 'POST',
                    body: JSON.stringify(output)
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result);
                    switch(result.rCode){
                        case 10:    // Successfull
                            console.log('<---------Upload stamps result ')
                            console.log(result);
                            document.getElementById('input-uploadStamp').value=""
                            view_StampList()
                            break;
                        case 40:    // Errors
                            alert(result.errorMsg);
                            break;
                    };
                });
            }
            r.readAsText(f);
        } else { 
            alert("Failed to load file");
        }
    }catch(e){
        console.error(e)
        alert(e)
    }
}

// Check stamps and evaluate 
function timeEvaluation(evt) {
    try{
        document.querySelector('#view-StampError').style.display = 'none';
        document.querySelector('#view-TimeResult').style.display = 'none';
        let today = new Date();
        let evaluationDay = prompt("Enter evaluation date in YYYY-MM-DD format",`${today.toISOString().split('T')[0]}`);
        
        var output = {
            date: evaluationDay
        };    
        // API route to send daily information
        console.log('Fetching to execute evaluation---------> ')
        fetch('/evaluation', {
            method: 'POST',
            body: JSON.stringify(output)
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
            switch(result.rCode){
                case 40:    // Errors
                    alert(result.errorMsg);
                    break;
                case 20:    // Show all stamp error details in a table
                    console.log('<---------Result of execute evaluation (Stamp errors)')
                    console.log(result)
                    document.querySelector('#tbody-StampError').innerHTML=""
                    result.body.forEach(stampError => {
                        let tr = document.createElement('tr');
                        let th = document.createElement('th');
                        let td1 = document.createElement('td');
                        let td2 = document.createElement('td');
                        let td3 = document.createElement('td');
                        let td4 = document.createElement('td');

                        // Populating fields
                        th.innerHTML = stampError.employeeId;
                        td1.innerHTML = stampError.day;
                        td2.innerHTML = stampError.stampType;
                        td3.innerHTML = stampError.timestamp;
                        td4.innerHTML = stampError.errorMessage;

                        // Nesting field into row
                        tr.append(th);
                        tr.append(td1);
                        tr.append(td2);
                        tr.append(td3);
                        tr.append(td4);

                        // Insert new row into table body
                        document.querySelector('#tbody-StampError').append(tr);
                        document.querySelector('#view-StampError').style.display = 'block';
                    });
                    break;
                case 10:    // Time evaluation results
                    console.log('<---------Result of execute evaluation (Evaluation results)')
                    console.log(result)
                    document.querySelector('#tbody-TimeResult').innerHTML=""
                    result.body.forEach(stampError => {
                        let tr = document.createElement('tr');
                        let th = document.createElement('th');
                        let td1 = document.createElement('td');
                        let td2 = document.createElement('td');
                        let td3 = document.createElement('td');
                        let td4 = document.createElement('td');

                        // Populating fields
                        th.innerHTML = stampError.employeeId;
                        td1.innerHTML = stampError.day;
                        td2.innerHTML = stampError.type;
                        td3.innerHTML = stampError.code;
                        td4.innerHTML = stampError.amount;

                        // Nesting field into row
                        tr.append(th);
                        tr.append(td1);
                        tr.append(td2);
                        tr.append(td3);
                        tr.append(td4);

                        // Insert new row into table body
                        document.querySelector('#tbody-TimeResult').append(tr);
                        document.querySelector('#view-TimeResult').style.display = 'block';
                    });
                    break;
            };
        });
    }catch(e){
        console.error(e)
        alert(e)
    }
}

  