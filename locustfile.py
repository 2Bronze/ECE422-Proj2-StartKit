from locust import HttpUser, LoadTestShape, task, constant

class NormalUser(HttpUser):
    wait_time = constant(1)

    @task
    def hello_world(self):
        self.client.get("/")

class BellCurveLoad(LoadTestShape):
    stages = [
        {"duration": 120, "users": 5, "spawn_rate": 5, "user_classes": [NormalUser]},
        {"duration": 240, "users": 10, "spawn_rate": 5, "user_classes": [NormalUser]},
        {"duration": 360, "users": 15, "spawn_rate": 5, "user_classes": [NormalUser]},
        {"duration": 480, "users": 10, "spawn_rate": 5, "user_classes": [NormalUser]},
        {"duration": 600, "users": 5, "spawn_rate": 5, "user_classes": [NormalUser]},
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