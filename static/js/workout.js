// let category = document.getElementById('workout_category').value;

document.getElementById('workout_category').addEventListener('change', function(){
    let liftingDiv = document.getElementById('lifting-div');
    let paceDiv = document.getElementById('pace-div');
    if(this.value == 'weight_lifting'){
        liftingDiv.style.display = 'block';
        paceDiv.style.display = 'none';
    }
    if(this.value != 'weight_lifting'){
        paceDiv.style.display = 'block';
        liftingDiv.style.display = 'none';
    }
})

// setInput(category);