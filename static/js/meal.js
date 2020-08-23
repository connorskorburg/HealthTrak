function updateFood(quantityID){
    console.log(quantityID);
    document.getElementById(quantityID).addEventListener('change', function(){
        let quantity  = parseFloat(document.getElementById(quantityID).value);
        let fatInput = document.querySelector(`#${quantityID}Form .fat`);
        let carbsInput = document.querySelector(`#${quantityID}Form .carbs`);
        let proteinInput = document.querySelector(`#${quantityID}Form .protein`);
    
        fatInput.value = parseFloat(fatInput.value) * quantity;
        carbsInput.value = parseFloat(carbsInput.value) * quantity;
        proteinInput.value = parseFloat(proteinInput.value) * quantity;
    })
}

updateFood("break");
updateFood("lunch");
updateFood("dinner");
updateFood("snack");
