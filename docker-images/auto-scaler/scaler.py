from docker import client
from flask import Flask, request, Response, jsonify, render_template
from flask_apscheduler import APScheduler
import requests
import time
import atexit
import sys

SERVICE_ID = sys.argv[1]

class Scaler:
    def __init__(self) -> None:
        self.client = client.DockerClient(base_url='unix://var/run/docker.sock')
        self.enabled = True
        self.replicas = 1
        
    def force_scale_to(self, service_id, replicas):
        service = self.client.services.get(service_id)
        service.scale(replicas)
    
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
        
app = Flask(__name__, template_folder="site", static_folder="site/static", static_url_path='/static')

response_times = {}
docker_replicas = {}
interval_times = []
scaler = Scaler()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def reset_replicas():
    scaler.force_scale_to(SERVICE_ID, 1)

INTERVAL_TASK_ID = 'interval-task-id'

def interval_task():
    now = time.time()
    requests.get('http://10.2.15.184:8000')
    end = time.time()
    print("RESPONSE TIME")
    print(end-now)
    response_times[time.time()] = end-now
    docker_replicas[time.time()] = scaler.replicas
    # if average_time > ???:
        # scaler.scale_up("docker_id")
    # elif average_time < ???:
        # scaler.scale_down("docker_id")


scheduler.add_job(id=INTERVAL_TASK_ID, func=interval_task, trigger='interval', seconds=2)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == "POST":
        interval_times.append(request.json["value"])
    else:
        res = jsonify({"response_times": response_times,
            "docker_replicas": docker_replicas
        })
        response_times.clear() # prevent sending same data twice
        docker_replicas.clear() # prevent sending same data twice
        return res
        

@app.route('/enable', methods=["POST"])
def enable():
    scaler.enable()
    return Response(status=200)

@app.route('/disable', methods=["POST"])
def disable():
    scaler.disable()
    return Response(status=200)

@app.route('/reset', methods=["POST"])
def reset():
    interval_times = []
    response_times = {}

if __name__ == "__main__":
    # reset to 1 if we ever exit
    atexit.register(reset_replicas)
    app.run(host="0.0.0.0", port=4444, debug=True)
    