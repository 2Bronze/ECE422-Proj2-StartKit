from docker import client
from flask import Flask, Response, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from time import time
import requests
import atexit
import gevent

class Scaler:
    def __init__(self) -> None:
        self.client = client.DockerClient(base_url='unix://var/run/docker.sock')
        self.service_id = ""
        for service in self.client.services.list():
            if service.name.find("web") >= 0:
                self.service_id = service.short_id
        self.enabled = True
        self.replicas = 1
        
    def force_scale_to(self, replicas):
        service = self.client.services.get(self.service_id)
        service.scale(replicas)
    
    def scale_up(self):
        if not self.enabled:
            return
        service = self.client.services.get(self.service_id)
        self.replicas += 1
        service.scale(self.replicas)
        
    def scale_down(self):
        if not self.enabled or self.replicas == 1:
            return
        service = self.client.services.get(self.service_id)
        self.replicas -= 1
        service.scale(self.replicas)
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
        
app = Flask(__name__, template_folder="site", static_folder="site/static", static_url_path='/static')

response_times = {}
docker_replicas = {}
scaler = Scaler()
scheduler = BackgroundScheduler()
isRecord = False

def reset_replicas():
    print("EXITED: Setting replicas to 1...")
    scaler.force_scale_to(1)
    print("EXITED: Set replicas to 1")

INTERVAL_TASK_ID = 'interval-task-id'
NUM_REQUESTS = 3
ACCEPTABLE_MAX = 5 # seconds
ACCEPTABLE_MIN = 2 # seconds

def get_response_time():
    now = time()
    requests.get('http://10.2.15.184:8000')
    end = time()
    return end-now


def interval_task():
    tasks = []
    tasks = [gevent.spawn(get_response_time) for _ in range(NUM_REQUESTS)]
    gevent.joinall(tasks)
    response = [task.value for task in tasks]
    
    average_response_time = sum(response)/len(response)
    print("RESPONSE TIME")
    print(average_response_time)
    if average_response_time > ACCEPTABLE_MAX:
        print("SCALING UP")
        scaler.scale_up()
    elif average_response_time < ACCEPTABLE_MIN:
        print("SCALING DOWN")
        scaler.scale_down()
    if not isRecord:
        return
    response_times[int(time()*1000)] = average_response_time
    docker_replicas[int(time()*1000)] = scaler.replicas


scheduler.add_job(id=INTERVAL_TASK_ID, func=interval_task, trigger='interval', seconds=10, max_instances=5)
scheduler.start()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    res = jsonify({
        "response_times": response_times,
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


@app.route('/current')
def current():
    return Response(str(scaler.enabled), status=200)

@app.route('/start', methods=["POST"])
def start():
    isRecord = True
    return Response(status=200)
    

@app.route('/stop', methods=["POST"])
def stop():
    isRecord = False
    response_times.clear()
    docker_replicas.clear()
    return Response(status=200)

if __name__ == "__main__":
    # reset to 1 if we ever exit
    atexit.register(reset_replicas)
    app.run(host="0.0.0.0", port=4444, debug=False) # disable debug to prevent launch 2 schedulers
    