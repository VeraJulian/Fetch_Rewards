# Fetch_Rewards
Fetch Rewards Coding Exercise - Backend Software Engineering

A unit test class is provided. To run, enter this on the command line:
	python test_rewards_api.py

It tests for adding transactions, spending points results, and checking balances.


To run a web server, enter this on the command line:
	python fetch_rewards_api.py

Note the port used is 8888

Add transactions and spend points through post requests. Examples in python: 

adding transaction:
requests.post('http://localhost:8888/api/add_transactions', data=json.dumps({ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }))

spending points:
requests.post('http://localhost:8888/api/spend_points', data=json.dumps({ "points": 5000 })).json()


Use get requests to retrieve balances:
requests.get('http://localhost:8888/api/get_balances').json()
