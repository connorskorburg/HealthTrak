// let category = document.getElementById('workout_category').value;

// console.log(category);


const selects = document.querySelectorAll('.workout_category');

console.log(selects);


selects.forEach(select => {
    select.addEventListener('change', function(){
    console.log(this.value);
    const liftingDiv = document.getElementById('lifting-div');
    const paceDiv = document.getElementById('pace-div');
    const otherDiv = document.getElementById('other-div');
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
});
// document.getElementById('workout_category').addEventListener('change', function(){
//     console.log(this.value);
//     const liftingDiv = document.getElementById('lifting-div');
//     const paceDiv = document.getElementById('pace-div');
//     const otherDiv = document.getElementById('other-div');
//     if(this.value == 'weight_lifting'){
//         liftingDiv.style.display = 'block';
//         paceDiv.style.display = 'none';
//         otherDiv.style.display = 'none';
//     }
//     if(this.value == 'other'){
//         otherDiv.style.display = 'block';
//         paceDiv.style.display = 'none';
//         liftingDiv.style.display = 'none';
//     }
//     if(this.value != 'weight_lifting' && this.value != 'other'){
//         paceDiv.style.display = 'block';
//         otherDiv.style.display = 'none';
//         liftingDiv.style.display = 'none';
//     }
// })

// setInput(category);
