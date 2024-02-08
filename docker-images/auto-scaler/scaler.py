from docker import client
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
import time

from flask import render_template

class Scaler:
    def __init__(self) -> None:
        self.client = client.DockerClient(base_url='unix://var/run/docker.sock')
        self.enabled = True
        self.replicas = 1
    
    def scale_up(self, service_id):
        if not self.enabled:
            return
        service = self.client.services.get(service_id)
        self.replicas += 10
        service.scale(self.replicas)
        
    def scale_down(self, service_id):
        if not self.enabled:
            return
        service = self.client.services.get(service_id)
        self.replicas -= 10
        service.scale(self.replicas)
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
        
app = Flask(__name__, template_folder="site")

response_times = {}
docker_replicas = {}
interval_times = []
scaler = Scaler()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

INTERVAL_TASK_ID = 'interval-task-id'
 
 
def interval_task():
    average_time = sum(interval_times)/len(interval_times)
    response_times[time.time()] = average_time
    docker_replicas[time.time()] = scaler.replicas
    # if average_time > ???:
        # scaler.scale_up("docker_id")
    # elif average_time < ???:
        # scaler.scale_down("docker_id")


scheduler.add_job(id=INTERVAL_TASK_ID, func=interval_task, trigger='interval', seconds=2)
 

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({
        response_times,
        docker_replicas
    })

@app.route('/receive', methods=["POST"])
def receive():
    interval_times.append(request.json["value"])

@app.route('/enable')
def enable():
    scaler.enable()

@app.route('/disable')
def disable():
    scaler.disable()

@app.route('/reset')
def reset():
    interval_times = []
    response_times = {}
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444, debug=True)
    