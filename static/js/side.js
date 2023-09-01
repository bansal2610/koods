// sidebar

function openNav() {
    document.getElementById("mySidebar").style.width = "314px";
    document.getElementById("main").style.marginLeft = "0px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

// sidebar end

// line chart

const xValues = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150];
const yValues = [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15];

new Chart("myChart1", {
    type: "line",
    data: {
        labels: xValues,
        datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues
        }]
    },
    options: {
        legend: { display: false },
        scales: {
            yAxes: [{ ticks: { min: 6, max: 16 } }],
        }
    }
});

// doughnut Chart

var xValuesdoughnut = ["Italy", "France", "Spain", "USA", "Argentina"];
var yValuesdoughnut = [55, 49, 44, 24, 115];
var barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

new Chart("myChart2", {
  type: "doughnut",
  data: {
    labels: xValuesdoughnut,
    datasets: [{
      backgroundColor: barColors,
      data: yValuesdoughnut
    }]
  },
  options: {
    title: {
      display: true,
      text: "Learnkoods"
    }
  }
});