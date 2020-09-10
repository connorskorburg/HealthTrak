
let mealBtns = document.querySelectorAll('.new-meal');
let mealForm = document.getElementById('meal-pop-outer');
console.log(mealBtns);

mealBtns.forEach(mealBtn => {
  mealBtn.addEventListener('click', () => {
    mealForm.style.display = 'block';
  })
});

document.getElementById('close-meal-form').addEventListener('click', () => {
  mealForm.style.display = 'none';
})


let dropdownButton = document.querySelectorAll('.dropdown-img')

// let x = document.querySelectorAll

function toggleForm(btns){
    btns.forEach(btn => {
        btn.addEventListener('click', function(){
            let cls = btn.getAttribute('data-alt-src');
            let meals = document.querySelectorAll(`.${cls}`);
            console.log(meals);
            meals.forEach(m => {
              if (m.style.display == 'none' || m.style.display == ''){
                  m.style.transition = 'all 550ms ease-in-out';
                  m.style.display = 'block';
                  btn.style.transform = 'scaleY(-1)';
                  btn.style.transition = 'all 150ms ease-in-out';
              }
              else {
                  m.style.display = 'none';
                  btn.style.transform = 'scaleY(1)';
                  btn.style.transition = 'all 150ms ease-in-out';
              }
            })
        });
    });
}

toggleForm(dropdownButton);