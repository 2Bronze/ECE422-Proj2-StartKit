from locust import HttpUser, LoadTestShape, task, between
import gevent

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")

class UserBehavior(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.ramp_up()

    @task
    def my_task(self):
        self.client.get("/")

    def ramp_up(self):
        for rps in range(1, 6):  # Incrementing the RPS every minute
            self.wait_time = between(60/rps, 60/rps)  # Adjusting the wait time
            gevent.sleep(60)  # Hold this RPS for 1 minute

        gevent.sleep(180)  # Hold the peak RPS for 3 minutes

        for rps in range(5, 0, -1):  # Decrementing the RPS every minute
            self.wait_time = between(60/rps, 60/rps)  # Adjusting the wait time
            gevent.sleep(60)  # Hold this RPS for 1 minute

class StagesShapeWithCustomUsers(LoadTestShape):

    stages = [
        {"duration": 120, "users": 5, "spawn_rate": 5, "user_classes": [QuickstartUser]},
        {"duration": 240, "users": 10, "spawn_rate": 5, "user_classes": [QuickstartUser]},
        {"duration": 360, "users": 15, "spawn_rate": 5, "user_classes": [QuickstartUser]},
        {"duration": 480, "users": 10, "spawn_rate": 5, "user_classes": [QuickstartUser]},
        {"duration": 600, "users": 5, "spawn_rate": 5, "user_classes": [QuickstartUser]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None