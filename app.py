import os
import logging

from flask import Flask, jsonify, request, Response
import numpy as np
app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def calculate_probabilities(start_value, end_value):
    k_values = np.arange(start_value, end_value+1)
    return list(k_values / (2 * k_values - 1))


app.logger.info("starting app")

env_start_value = int(os.environ.get('START_VALUE'))
env_end_value = int(os.environ.get('END_VALUE'))

probabilities = calculate_probabilities(env_start_value, env_end_value)

app.logger.info("result array calculated")


@app.route('/probabilities', methods=['GET'])
def get_probabilities():
    k = request.headers.get('k')
    app.logger.info(f"/probabilities received request with k={k}")

    if k is None:
        return jsonify({'probabilities': probabilities})

    try:
        k = int(k)
        if 6 <= k <= 99:
            return jsonify({'probability': probabilities[k - 6]})
        else:
            return Response('Value out of range', status=400)

    except ValueError:
        return Response('Invalid value for "k"', status=400)


if __name__ == "__main__":
    app.run(debug=True)
