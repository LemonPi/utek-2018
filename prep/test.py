import random
import math
from collections import OrderedDict

SEED = 1
random.seed(SEED)

INPUT = "terrain.txt"
arrays = []
# load data
with open(INPUT, 'r') as fin:
    for line in fin:
        arrays.append([float(num) for num in line.split(",")[:-1]])

neighbours = ((1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1))

# how many numbers we're allowed to query
MAX_STEPS = 1000
MAX_TEMPERATURE = 1
BASE_SELECTIVITY = 2


def pick_state(current_score, new_score, temperature, max_temperature, base_selectivity):
    """Assign a probability to picking the new state over the current state as a function of temperature.
    Must return a value [0,1]
    """

    # the lower the temperature the more selective we are about decreasing resolution
    selectivity = base_selectivity - temperature / max_temperature

    # good if positive
    score_gain = new_score - current_score

    if score_gain > 0:
        return 1

    # print("resolution gain: {}".format(score_gain))
    prob = 1 / (1 + math.exp(-selectivity * score_gain))
    print("probability: {}".format(prob))

    # apply sloped sigmoid function, which guarantees to be (0,1)
    return prob


def anneal(temperature, step):
    # cool down (really crude scheduling)
    return temperature * 0.98


def getNeighbour(currentState, neighbourHood, isValid):
    while True:
        movement = neighbourHood[random.randint(0, len(neighbourHood) - 1)]
        newState = tuple(a + b for (a, b) in zip(currentState, movement))
        # check if valid state
        if isValid(newState):
            return newState


def isStateValid(state):
    (r, c) = state
    return r >= 0 and r < len(arrays) and c >= 0 and c < len(arrays[0])


def main():
    # initialize temperature
    temperature = MAX_TEMPERATURE

    # assign initial state
    # random initial starting location
    r = random.randint(0, len(arrays) - 1)
    c = random.randint(0, len(arrays[0]) - 1)

    # track score over time
    scores = OrderedDict()
    # keep the best resolution for printing at the end
    best_score = arrays[r][c]
    best_state = (r, c)

    step = 0
    while step < MAX_STEPS:
        # score current state (only care about maximum per location)
        current_score = arrays[r][c]
        # track score
        scores[step] = current_score
        print(temperature, current_score)

        # pick random neighbour
        (rr, cc) = getNeighbour((r, c), neighbours, isStateValid)
        new_score = arrays[rr][cc]
        if pick_state(current_score, new_score, temperature, MAX_TEMPERATURE, BASE_SELECTIVITY) > random.random():
            r = rr
            c = cc
            if new_score > best_score:
                best_score = new_score
                best_state = (r, c)

        print("step {} \tbest {}".format(step, best_score))

        temperature = anneal(temperature, step)
        step += 1

    print("best score (annealing): {}".format(best_score))
    print("best score: {}".format(max(max(arr) for arr in arrays)))

if __name__ == "__main__":
    main()