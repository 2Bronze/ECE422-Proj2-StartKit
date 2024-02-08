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
        .then(({data}) => {
            console.log(data)
            responseLabels.push(Object.keys(data.response_times).map((time) => new Date(time)))
            responseTime.push(Object.values(data.response_times))
            replicasLabels.push(Object.keys(data.docker_replicas).map((time) => new Date(time)))
            replicas.push(Object.values(data.docker_replicas))
            responseTimeChart.update()
            replicasChart.update()
        })
}

const addData = () => {
    responseLabels.push("ALRIGHT")
    responseTime.push(5)
    replicasLabels.push("ALRIGHT")
    replicas.push(5)
    responseTimeChart.update()
    replicasChart.update()
}