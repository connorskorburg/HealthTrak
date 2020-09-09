let caloriesConsumed = parseFloat(document.getElementById('calories_consumed').value)
let caloriesBurned = parseFloat(document.getElementById('calories_burned').value)
let caloriesDaily = parseFloat(document.getElementById('daily_calories').value)

Chart.defaults.global.legend.display = false;

const colors = ['#e682fd','#c8b2f7']

var perc = 75;


function addText() {

    var canvas = document.getElementById("myChart");
    var ctx = document.getElementById("myChart").getContext("2d");
  
    var cx = canvas.width / 2;
    var cy = canvas.height / 2;
  
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '50px verdana';
    ctx.fillStyle = 'black';
    ctx.fillText("Text Here", cx, cy);
  
  }


var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'doughnut',

    // The data for our dataset
    data: {
        labels: ['Daily Average Calories','Calories Consumed'],
        datasets: [{
            label: 'Daily Log',
            // backgroundColor: 'rgb(255, 99, 132)',
            backgroundColor: colors,
            borderColor: colors,
            data: [caloriesDaily, caloriesConsumed]
        }]
    },
    // Configuration options go here
    options: {
        responsive: true,
        animation: {
            animateScale: true,
            animateRotate: true,
        },
        onAnimationComlete: addText,
        
    }
});