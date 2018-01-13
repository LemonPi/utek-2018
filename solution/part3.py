import part1
import part2
import random
import math
from utekutils import doPart, asciiForA, asciiForZ, ptb_prob_weights
from collections import OrderedDict



def crack3a(ciphertext):
    bestScore = -1
    bestText = None
    bestKey = -1
    for i in range(0, 26):
        newText = part1.encryptBlock(ciphertext, [i], False)
        newScore = part2.get_ptb_sentence_score(newText, ptb_prob_weights)
        if newScore > bestScore:
            bestScore = newScore
            bestText = newText
            bestKey = i
    return str(bestKey) + " | " + bestText

## functions for 3B

# how many numbers we're allowed to query
MAX_STEPS = 1000
MAX_TEMPERATURE = 1
BASE_SELECTIVITY = 2

SEED = 1
random.seed(SEED)


def pick_state(curr_score, new_score, temperature, max_temperature, base_selectivity):
    """Assign a probability to picking the new state over the current state as a function of temperature.
    Must return a value [0,1]
    """

    # the lower the temperature the more selective we are about decreasing resolution
    selectivity = base_selectivity - temperature / max_temperature

    # good if positive
    score_gain = new_score - curr_score

    if score_gain > 0:
        return 1

    # print("resolution gain: {}".format(score_gain))
    prob = 1 / (1 + math.exp(-selectivity * score_gain))
    #print("probability: {}".format(prob))

    # apply sloped sigmoid function, which guarantees to be (0,1)
    return prob


def anneal(temperature, step):
    # cool down (really crude scheduling)
    return temperature * 0.98


def getNeighbour(curr_key, isValid):
    # 26^(key length) possible keys
    # 2*(key length) possible neighbors (+1, -1 for each key[i])

    N = len(curr_key)
    new_key = list(curr_key)

    while True:
        i = random.randint(0, N-1)
        new_key[i] = (new_key[i] + random.choice([-1, 1])) % 26
        # check if valid state
        # if isValid(new_key):
        #    return tuple(new_key)


def isStateValid(key):
    N = len(key)

    for i in key:
        if i < 0 or i > 26:
            return False
    return True


def score(key, scores_dp, sentence):

    # if this score has already been calculated, just return it
    if key in scores_dp:
        return scores_dp[key]

    # else, calculate the score and return it
    dcr_sentence = part1.encryptBlock(sentence, list(key), False) # from part 1
    return part2.get_ptb_sentence_score(dcr_sentence, ptb_prob_weights) # from part 2


def crack3b(ciphertext):
    # initialize temperature
    temperature = MAX_TEMPERATURE

    # assign initial state
    # random initial starting location
    # r = random.randint(0, len(arrays) - 1)
    # c = random.randint(0, len(arrays[0]) - 1)

    # parse the input
    sentence = ciphertext[4:] # get rid of the 'number | '
    sentence = part2.sanitize_input(sentence)

    key_length = int(ciphertext[0])

    curr_key = []
    for i in range(0, key_length):
        curr_key.append(random.randint(0, 26))

    curr_key = tuple(curr_key)



    #weights = [1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,0.888889]

    # track score over time
    scores_dp = OrderedDict()

    ## for testing the prep case
#    for i in range(0, 99):
#        for j in range(0, 99):
#            scores_dp[(i, j)] = arrays[i][j]

    # keep the best resolution for printing at the end
    best_score = score(curr_key, scores_dp, sentence)
    best_key = curr_key

    step = 0
    while step < MAX_STEPS:
        # score current state (only care about maximum per location)
        curr_score = score(curr_key, scores_dp, sentence)
        # track score
        scores_dp[curr_key] = curr_score
        #print(temperature, curr_score)

        # pick random neighbour
        new_key = getNeighbour(curr_key, isStateValid)
        new_score = score(new_key, scores_dp, sentence)
        if pick_state(curr_score, new_score, temperature, MAX_TEMPERATURE, BASE_SELECTIVITY) > random.random():
            curr_key = new_key
            if new_score > best_score:
                best_score = new_score
                best_key = new_key

        #print("step {} \tbest {}".format(step, best_score))

        temperature = anneal(temperature, step)
        step += 1

    print("best score (annealing): {}".format(best_score))
    #print("best score: {}".format(max(max(arr) for arr in arrays)))
    print("best key: {}".format(best_key))
    print(part1.encryptBlock(sentence, list(best_key), True))



def main():
    #doPart("3a", crack3a)
    doPart("3b", crack3b)

if __name__ == "__main__":
    main()
