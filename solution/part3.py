import part1
import part2
import random
import math
from utekutils import doPart, asciiForA, asciiForZ, ptb_prob_weights, inf
from collections import OrderedDict



def crack3a(ciphertext):
    bestScore = -inf
    bestText = None
    bestKey = -1
    for i in range(0, 26):
        newText = part1.encryptBlock(ciphertext, [i], False)
        newScore = part2.get_ptb_sentence_score(part2.sanitize_input(newText), ptb_prob_weights)
        if newScore > bestScore:
            bestScore = newScore
            bestText = newText
            bestKey = i
    return str(bestKey) + " | " + bestText

## functions for 3B

# how many numbers we're allowed to query
MAX_STEPS = 10000
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
    score_gain = (new_score - curr_score) * 0.1

    if score_gain > 0:
        return 1

    # print("resolution gain: {}".format(score_gain))
    prob = 1 / (1 + math.exp(-selectivity * score_gain))
    print("{} -> {} probability: {}".format(curr_score, new_score, prob))

    # apply sloped sigmoid function, which guarantees to be (0,1)
    return prob


def anneal(temperature, step):
    # cool down (really crude scheduling)
    return temperature * 0.98


def getNeighbour(curr_key, isValid):
    # 26^(key length) possible keys
    # 2*(key length) possible neighbors (+1, -1 for each key[i])

    N = len(curr_key)

    i = random.randint(0, N-1)
    change = (curr_key[i] + random.randint(1,26)) % 26

    return tuple(curr_key[k] if k != i else change for k in range(N))


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
    dcr_sentence = part1.encryptBlock(sentence, key, False) # from part 1
    return part2.get_ptb_sentence_score(dcr_sentence, ptb_prob_weights) # from part 2


def crack3b(ciphertext):
    # initialize temperature
    temperature = MAX_TEMPERATURE

    # assign initial state
    # random initial starting location
    # r = random.randint(0, len(arrays) - 1)
    # c = random.randint(0, len(arrays[0]) - 1)

    ciphertext = [text.strip() for text in ciphertext.split("|")]
    # parse the input
    orig_sentence = ciphertext[1]
    sentence = part2.sanitize_input(orig_sentence)

    key_length = int(ciphertext[0])

    curr_key = tuple(random.randint(0, 26) for _ in range(key_length))

    # track score over time
    scores_dp = OrderedDict()

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
    print(part1.encryptBlock(sentence, list(best_key), False))
    return " ".join([" ".join((str(k) for k in best_key)),"|", part1.encryptBlock(orig_sentence, best_key, False)])


def main():
    #doPart("3a", crack3a)
    doPart("3b", crack3b)

if __name__ == "__main__":
    main()
