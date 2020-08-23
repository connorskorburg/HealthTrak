// let category = document.getElementById('workout_category').value;

document.getElementById('workout_category').addEventListener('change', function(){
    let liftingDiv = document.getElementById('lifting-div');
    let paceDiv = document.getElementById('pace-div');
    let otherDiv = document.getElementById('other-div');
    if(this.value == 'weight_lifting'){
        liftingDiv.style.display = 'block';
        paceDiv.style.display = 'none';
        otherDiv.style.display = 'none';
    }
    if(this.value == 'other'){
        otherDiv.style.display = 'block';
        paceDiv.style.display = 'none';
        liftingDiv.style.display = 'none';
    }
    if(this.value != 'weight_lifting' && this.value != 'other'){
        paceDiv.style.display = 'block';
        otherDiv.style.display = 'none';
        liftingDiv.style.display = 'none';
    }
})

// setInput(category);
