#!/usr/bin/env python3
"""
This is a locust file written in python to be used for load testing a kubernetes based
API running on my at-home hardware.
"""
import random
import string
from typing import List
from locust import HttpUser, task, between


def get_random_scoreboard() -> str:
    """Generate a random, yet legal value for a scoreboard name"""
    min_length = 4
    max_length = 12
    allowed_characters = string.ascii_lowercase + "-"
    return "".join(
        random.choices(allowed_characters, k=random.randint(min_length, max_length))
    )


def get_random_players() -> List[str]:
    """Generates a random set of usernames for a scoreboard"""
    random_names = [
        "Jimmy Neutron",
        "Spongebob Squarepants",
        "Abradolf Lincler",
        "Rick Sanchez",
        "Zim",
        "Louise",
        "Thelma",
        "Bugs Bunny",
        "Pea Tear Griffin",
        "Bob Sagat",
        "Steven Segal",
        "Phineas",
        "BMW",
        "Ligma",
        "Ghost Rider",
        "A small hairy pickle",
        "Nobody asked you...",
    ]
    return list(
        set(random.choices(random_names, k=random.randint(2, len(random_names))))
    )


class ScoreboardUser(HttpUser):
    wait_time = between(0.1, 2)
    scoreboard = get_random_scoreboard()
    players = get_random_players()
    scoreboard_endpoint = "/api/scoreboard/" + scoreboard

    def on_start(self):
        self.client.get(self.scoreboard_endpoint)
        for player in self.players:
            self.client.post(
                self.scoreboard_endpoint + "/score/" + player, json={"score": 0}
            )

    @task(80)
    def get_scoreboard(self):
        self.client.get(self.scoreboard_endpoint)

    @task(15)
    def change_score(self):
        if self.players:
            player = random.choice(self.players)
            self.client.put(
                self.scoreboard_endpoint + "/score/" + player,
                json={
                    "score": random.randint(-1000, 1000),
                    "method": random.choice(["add", "replace"]),
                },
            )
        else:
            self.players = get_random_players()
            for player in self.players:
                self.client.post(
                    self.scoreboard_endpoint + "/score/" + player, json={"score": 0}
                )

    @task(5)
    def change_player_list(self):
        try:
            delete_player = self.players.pop()
            self.client.delete(self.scoreboard_endpoint + "/score/" + delete_player)
        except IndexError:
            print("Player list empty...")
        new_player = get_random_players()[0]
        self.client.post(
            self.scoreboard_endpoint + "/score/" + new_player,
            json={"score": random.randint(-1000, 1000)},
        )
        if new_player not in self.players:
            self.players.append(new_player)

    @task(5)
    def clear_scoreboard(self):
        self.client.put(self.scoreboard_endpoint)

    def on_stop(self):
        self.client.delete(self.scoreboard_endpoint)
