let today = new Date()
let currentMonth = today.getMonth()
let currentYear = today.getFullYear()
let months = ["Jan", "Feb", "Mar", "Apr","May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];

let logs = document.getElementById('logs');
let parsedLogs = JSON.parse(logs.textContent);

showCal(currentMonth, currentYear);

function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCal(currentMonth, currentYear);
}
function previous(){
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth -1;
    showCal(currentMonth, currentYear);
}

function showCal(month, year){
    let firstDay = new Date(year, month).getDay();
    let daysInMonth = 32 - new Date(year, month, 32).getDate()
    let date = 1;
    
    let calContent = document.getElementById('cal-content');
    let showMonth = document.getElementById('month');
    let showYear = document.getElementById('year');
    
    calContent.innerHTML = "";

    showMonth.textContent = months[`${month}`];
    showYear.textContent = year;
    
    
    for(let i = 0; i < 6; i++){
        let row = document.createElement('tr');
        for(let x = 0; x < 7; x ++){
            if(i===0 && x < firstDay){
                let td = document.createElement('td');
                let p = document.createElement('p');
                p.appendChild(document.createTextNode(""));
                td.appendChild(p);
                row.appendChild(td);
            } else if(date > daysInMonth) {
                break;
            } else {
                let td = document.createElement('td');
                let p = document.createElement('p');
                p.appendChild(document.createTextNode(date));
                if(date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                    td.classList.add("bg-info");
                }
                parsedLogs.forEach(log => {
                    let created = new Date(log.created_at);
                    if(date === created.getDate() && year === created.getFullYear() && month === created.getMonth()){
                        td.classList.add('log-td');
                        let button = document.createElement('button');
                        button.setAttribute("onclick", `showLog(${log.id})`)
                        button.classList.add('log-btn');
                        p.appendChild(button);
                    }  
                });
                td.appendChild(p);
                row.appendChild(td)
                date++;
            }
        }
        calContent.appendChild(row);
    }
}

function showLog(id) {
    parsedLogs.forEach(log => {
        let created = new Date(log.created_at);
        if(id == log.id){
            console.log(log.minutes_worked_out);
            let popup = document.getElementById('log-pop-outer');
            popup.style.display = 'block';
            let date = document.getElementById('log-date');
            let calories_burned = document.getElementById('calories_burned');
            let calories_consumed = document.getElementById('calories_consumed');
            let minutes_worked_out = document.getElementById('minutes_worked_out');
            date.textContent = months[created.getMonth()] + " " + created.getDate();
            calories_burned.textContent = log.calories_burned;
            calories_consumed.textContent = log.calories_consumed;
            minutes_worked_out.textContent = log.minutes_worked_out;
        }
    })
}

function hideLog(){
    let popup = document.getElementById('log-pop-outer');
    popup.style.display = 'none';
}