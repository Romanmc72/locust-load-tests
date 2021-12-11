#!/usr/bin/env python3
"""
This is a locust file written in python to be used for load testing a lambda
function running on AWS API Gateway.
"""
import time
from locust import HttpUser, task, between


class FakeDataUser(HttpUser):
    wait_time = between(0.1, 2)

    @task
    def get_documentation(self):
        self.client.get("/docs")

    @task(3)
    def get_fake_data(self):
        self.client.get("/")

    @task(1)
    def get_custom_fake_data_error(self):
        self.client.post("/", json={"schematic": {"hot_dogs": "dog"}})

    @task(10)
    def get_custom_fake_data(self):
        self.client.post(
            "/",
            json={
                "schematic": {
                    "person_id": "uuid4",
                    "poops_per_year": "pyint",
                    "biggest_poop": "date",
                    "latest_poop": "time",
                }
            },
        )
