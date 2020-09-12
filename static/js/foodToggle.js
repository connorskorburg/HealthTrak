const results = document.getElementById('hidden-results');
console.log(results);

const parsedResults = JSON.parse(results.textContent);

const searchPopOuter = document.querySelector('.search-pop-outer');

const fatResults = document.querySelector('.fat-results');
const carbsResults = document.querySelector('.carbs-results');
const proteinResults = document.querySelector('.protein-results');
const calResults = document.querySelector('.cal-results');
const descResults = document.querySelector('.desc-results');
const closeResForm = document.getElementById('close-res-form');


closeResForm.addEventListener('click', () => {
  searchPopOuter.style.display = 'none';
})

const myBtns = document.querySelectorAll('.res-btn');

myBtns.forEach(btn => {
  btn.addEventListener('click', ()=> {
    parsedResults.forEach(r => {
      if(parseFloat(r.id) == parseFloat(btn.getAttribute('data-alt-cls'))){
        descResults.value = r.description;
        fatResults.value = r.fat;
        carbsResults.value = r.carbs;
        proteinResults.value = r.protein;
        const calories = parseFloat(r.fat * 9) + parseFloat(r.carbs * 4) + parseFloat(r.protein * 4);
        calResults.value = calories.toFixed(2);
        searchPopOuter.style.display = 'block';
        
      }
    })
  })
});

