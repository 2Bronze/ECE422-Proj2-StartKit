let ctx = document.getElementById('response');

let responseTime = []
let replicas = []

const responseTimeChart = new Chart(ctx, {
type: 'line',
data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
    label: '# of Votes',
    data: responseTime,
    borderWidth: 1
    }]
},
options: {
    responsive: true,
    plugins: {
        title: {
          display: true,
          text: 'Chart.js Line Chart'
        }
    },
    scales: {
        y: {
            beginAtZero: true
        }
    }
}
});


ctx = document.getElementById('replicas');

const replicasChart = new Chart(ctx, {
type: 'bar',
data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
    label: '# of Votes',
    data: replicas,
    borderWidth: 1
    }]
},
options: {
    scales: {
    y: {
        beginAtZero: true
    }
    }
}
});

const pingForData = () => {
    axios.get("http://localhost:4444/data")
        .then((data) => {
            console.log(data)
            responseTime.push()
            replicas.push()
        })
}

const addData = () => {
    responseTime.push(5)
    replicas.push(5)
    responseTimeChart.update()
    replicasChart.update()
}