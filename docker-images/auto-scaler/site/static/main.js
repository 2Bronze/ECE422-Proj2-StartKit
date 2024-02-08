let ctx = document.getElementById('response');

let responseTime = []
let replicas = []
let responseLabels = []
let replicasLabels = []

const responseTimeChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: responseLabels,
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
    type: 'line',
    data: {
        labels: replicasLabels,
        datasets: [{
        label: '# of Votes',
        data: replicas,
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

const enableScaling = () => {
    axios.post("http://10.2.15.184:4444//enable")
}

const disableScaling = () => {
    axios.post("http://10.2.15.184:4444//disable")
}

const pingForData = () => {
    axios.get("http://10.2.15.184:4444/data")
        .then((data) => {
            console.log(data)
            responseLabels = Object.keys(data.response_times)
            responseTime = Object.values(data.response_times)
            replicasLabels = Object.keys(data.docker_replicas)
            replicas = Object.values(data.docker_replicas)
        })
}

const addData = () => {
    responseTime.push(5)
    replicas.push(5)
    responseTimeChart.update()
    replicasChart.update()
}