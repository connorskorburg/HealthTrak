let mealBtns = document.querySelectorAll('.meal p')
let workoutBtns = document.querySelectorAll('.workout p')

function toggleForm(btns){
    btns.forEach(btn => {
        btn.addEventListener('click', function(){
            let id = btn.getAttribute('data-alt-src');
            let form = document.getElementById(id);
            if (form.style.display == 'none' || form.style.display == ''){
                form.style.display = 'block';
            }
            else {
                form.style.display = 'none';
            }
        });
    });
}

toggleForm(mealBtns);
toggleForm(workoutBtns);