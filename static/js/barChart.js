
let fat = parseFloat(document.getElementById('daily_fat').value);
let protein = parseFloat(document.getElementById('daily_protein').value);
let carbs = parseFloat(document.getElementById('daily_carbs').value);

console.log(fat);
console.log(protein);
console.log(carbs);

let ctx2 = document.getElementById('barChart').getContext('2d');
let myBarChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Fat', 'Protein', 'Carbs'],
        datasets: [{
            label: 'Daily Log',
            data: [fat, protein, carbs],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ]
        }]
    },
    options: {
        responsive: true,
        animation: {
            animateScale: true,
            animateRotate: true,
        },
        onAnimationComlete: addText,
        scales: {
            yAxes: [{
                ticks: {
                    min: 0
                }
            }],
            xAxes: [{
                display: false
            }]
        }
    }
});