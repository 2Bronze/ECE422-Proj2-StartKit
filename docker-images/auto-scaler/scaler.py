from docker import client
from flask import Flask, request, Response, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
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
        self.replicas += 1
        service.scale(self.replicas)
        
    def scale_down(self, service_id):
        if not self.enabled or self.replicas == 1:
            return
        service = self.client.services.get(service_id)
        self.replicas -= 1
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
scheduler = BackgroundScheduler()

def reset_replicas():
    print("EXITED: Setting replicas to 1...")
    scaler.force_scale_to(SERVICE_ID, 1)
    print("EXITED: Set replicas to 1")

INTERVAL_TASK_ID = 'interval-task-id'
NUM_REQUESTS = 3
ACCEPTABLE_MAX = 5 # seconds
ACCEPTABLE_MIN = 3 # seconds

def interval_task():
    now = time.time()
    for _ in range(NUM_REQUESTS):
        requests.get('http://10.2.15.184:8000')
    end = time.time()
    average_response_time = (end-now)/NUM_REQUESTS
    print("RESPONSE TIME")
    print(average_response_time)
    if average_response_time > ACCEPTABLE_MAX:
        print("SCALING UP")
        scaler.scale_up(SERVICE_ID)
    elif average_response_time < ACCEPTABLE_MIN:
        print("SCALING DOWN")
        scaler.scale_down(SERVICE_ID)
    now = datetime.now()
    response_times[int(time.time_ns()//1000)] = average_response_time
    docker_replicas[int(time.time_ns()//1000)] = scaler.replicas


scheduler.add_job(id=INTERVAL_TASK_ID, func=interval_task, trigger='interval', seconds=10, max_instances=5)
scheduler.start()


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
    