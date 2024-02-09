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
            console.log(Object.keys(data.response_times))
            console.log(Object.keys(data.response_times).map((time) => (new Date(parseInt(time))).toLocaleString("en-US")))
            responseLabels.push(...Object.keys(data.response_times).map((time) => (new Date(parseInt(time))).toLocaleString("en-US")))
            responseTime.push(...Object.values(data.response_times))
            replicasLabels.push(...Object.keys(data.docker_replicas).map((time) => (new Date(parseInt(time))).toLocaleString("en-US")))
            replicas.push(...Object.values(data.docker_replicas))
            responseTimeChart.update()
            replicasChart.update()
        })
}

setInterval(pingForData, 10000)

const addData = () => {
    responseLabels.push("ALRIGHT")
    responseTime.push(5)
    replicasLabels.push("ALRIGHT")
    replicas.push(5)
    responseTimeChart.update()
    replicasChart.update()
}