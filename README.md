# dice_app
application to return probabilities of outcomes in a dice game

# prerequisites
Docker must be installed and running on your local machine

# running unit tests
from the top directory of this repository, run:

```
docker compose up test --build
```

# running app
```
docker compose up myapp --build
```

see docker-compose.yml file for to set environment variables and port options. Currently, START_VALUE=6, END_VALUE=99, and PORT=5000

context:
Bob and Alice take turns rolling a k-sided die (Bob rolls first). Whoever rolls a k value wins

endpoints:

GET url http://localhost:PORT/probabilities - returns {"probabilities: [probability of Bob winning game given a k-sided die for k between START_VALUE and END_VALUE]}, code: 200

GET url http://localhost:PORT/probabilities headers = {'k': k} - returns {"probability: probability of Bob winning game given a k-sided die}, code: 200
(if k is not an integer with START_VALUE <= k <= END_VALUE, returns 400 error code with error message response body)

# notes
app calculates probability P that Bob wins game given a k-sided die with the following equation:

```
P = k / (2*k - 1)
```

This can be derived from observing that 
```
P = 1/k (probability Bob wins on first turn) + ((k-1)/k)*((k-1)/k) (probability Bob does not win on first turn * probability Alice does not win on first turn) * P (probability Bob wins in a later round)
```

