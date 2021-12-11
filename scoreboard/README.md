# Locust Test Scoreboard API

This is designed to load test my API and to see how the performance degrades (or doesn't) under a certain number of users.

## Running The Test

Launch the test stack with `./up.sh` and bring it down with `./down.sh`.

Once it is launched, go to [localhost](http://localhost:8089) and enter the number of concurrent users, the spawn rate, and the url for the API. In my case that url is `https://scoreboard.r0m4n.com`. Then hit go and watch the magic happen!

## Expected Results

This should, based on my tests, be able to support several hundred concurrent users without issue. The median response times are typically right around 10 ms, and the failure rate is expected to be around 4% given the test has intentional calls to an endpoint that will produce a 400 error every time (because it tries to create a player that already exists).
