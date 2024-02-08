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
            text: 'Response Time'
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
              text: 'Web Replicas'
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
    axios.post("http://10.2.15.184:4444/enable")
}

const disableScaling = () => {
    axios.post("http://10.2.15.184:4444/disable")
}

const pingForData = () => {
    axios.get("http://10.2.15.184:4444/data")
        .then(({data}) => {
            console.log(data)
            responseLabels.push(...Object.keys(data.response_times))
            responseTime.push(...Object.values(data.response_times))
            replicasLabels.push(...Object.keys(data.docker_replicas))
            replicas.push(...Object.values(data.docker_replicas))
            responseTimeChart.update()
            replicasChart.update()
        })
}

setInterval(pingForData, 5000)

const addData = () => {
    responseLabels.push("ALRIGHT")
    responseTime.push(5)
    replicasLabels.push("ALRIGHT")
    replicas.push(5)
    responseTimeChart.update()
    replicasChart.update()
}