import json

with open('users.json') as file:
  data = json.load(file)

  for user in data:
    print(data[user]['puntajes'])
