let results = document.getElementById('hidden-results');
console.log(results);

let parsedResults = JSON.parse(results.textContent);


let myBtns = document.querySelectorAll('.res-btn');
// document.querySelector('.res-btn').addEventListener('onclick', () => {
  // console.log("hello");
// })

myBtns.forEach(btn => {
  console.log(btn);
});

console.log(myBtns);
console.log(parsedResults);