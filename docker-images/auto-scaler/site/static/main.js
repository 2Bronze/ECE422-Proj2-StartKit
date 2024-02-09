let ctx = document.getElementById('response');

let responseTime = []
let replicas = []
let responseLabels = []
let replicasLabels = []

let scalerStatus = true
let scalarStatusUI = document.getElementById('status')



const responseTimeChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: responseLabels,
        datasets: [{
            label: 'Response Time (s)',
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
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Response Time (s)'
                }
            }
        },
    }
});


ctx = document.getElementById('replicas');

const replicasChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: replicasLabels,
        datasets: [{
        label: '# of Replicas',
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
            },
            legend: {
                display: false,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,
                },
                title: {
                    display: true,
                    text: '# of Replicas'
                }
            }
        }
    }
});

const enableScaling = () => {
    axios.post("http://10.2.15.184:4444/enable")
        .then(() => {
            if (scalarStatusUI)
                scalarStatusUI.classList.replace('disabled', 'enabled')
        })
}

const disableScaling = () => {
    axios.post("http://10.2.15.184:4444/disable")
        .then(() => {
            if(scalarStatusUI)
                scalarStatusUI.classList.replace('enabled', 'disabled')
        })
}

const pingForData = () => {
    axios.get("http://10.2.15.184:4444/data")
        .then(({data}) => {
            responseLabels.push(...Object.keys(data.response_times).map((time) => (new Date(parseInt(time))).toLocaleTimeString("en-US")))
            responseTime.push(...Object.values(data.response_times))
            replicasLabels.push(...Object.keys(data.docker_replicas).map((time) => (new Date(parseInt(time))).toLocaleTimeString("en-US")))
            replicas.push(...Object.values(data.docker_replicas))
            responseTimeChart.update()
            replicasChart.update()
        })
}

setInterval(pingForData, 10000)

const fetchCurrentData = () => {
    axios.get("http://10.2.15.184:4444/current")
        .then(({data}) => {
            responseLabels.push(...Object.keys(data.response_times).map((time) => (new Date(parseInt(time))).toLocaleTimeString("en-US")))
            responseTime.push(...Object.values(data.response_times))
            replicasLabels.push(...Object.keys(data.docker_replicas).map((time) => (new Date(parseInt(time))).toLocaleTimeString("en-US")))
            replicas.push(...Object.values(data.docker_replicas))
            responseTimeChart.update()
            replicasChart.update()
        })
}

const resetData = () => {
    axios.post("http://10.2.15.184:4444/reset")
    responseTime.splice(0, responseTime.length)
    replicas.splice(0, replicas.length)
    responseLabels.splice(0, responseLabels.length)
    replicasLabels.splice(0, replicasLabels.length)
}