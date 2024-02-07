from docker import client
import sys
import time


class Scaler:
    def __init__(self) -> None:
        self.client = client.DockerClient(base_url='unix://var/run/docker.sock')
        self.replicas = 1
    
    def scale_up(self, service_id):
        service = self.client.services.get(service_id)
        self.replicas += 10
        service.scale(self.replicas)
        
    def scale_down(self, service_id):
        service = self.client.services.get(service_id)
        self.replicas -= 10
        service.scale(self.replicas)
        
        
        
if __name__ == "__main__":
    id = sys.argv[1]
    print(id)
    scaler = Scaler()
    print("Scaled Up")
    scaler.scale_up(id)
    
    time.sleep(60)
    
    print("Scaled Down")
    scaler.scale_down(id)
    