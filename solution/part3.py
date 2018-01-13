import part1
import part2
import random
import math
from utekutils import doPart, asciiForA, asciiForZ, ptb_prob_weights, inf
from collections import OrderedDict
import time


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
MAX_STEPS = 1000
MAX_TEMPERATURE = 1
BASE_SELECTIVITY = 2

SEED = 1
random.seed(SEED)


def pick_state(curr_score, new_score, temperature, max_temperature, base_selectivity, score_scale):
    """Assign a probability to picking the new state over the current state as a function of temperature.
    Must return a value [0,1]
    """

    # the lower the temperature the more selective we are about decreasing resolution
    selectivity = base_selectivity - temperature / max_temperature

    # good if positive
    score_gain = (new_score - curr_score) * score_scale

    if score_gain > 0:
        return 1

    # print("resolution gain: {}".format(score_gain))
    prob = 1 / (1 + math.exp(-selectivity * score_gain))
    # print("{} -> {} probability: {}".format(curr_score, new_score, prob))

    # apply sloped sigmoid function, which guarantees to be (0,1)
    return prob


def anneal(temperature, step):
    # cool down (really crude scheduling)
    return temperature * 0.98


def get_neighbour_block_key(curr_key, isValid):
    # 26^(key length) possible keys
    # 2*(key length) possible neighbors (+1, -1 for each key[i])

    N = len(curr_key)

    i = random.randint(0, N - 1)
    change = (curr_key[i] + random.randint(1, 26)) % 26

    return tuple(curr_key[k] if k != i else change for k in range(N))


def isStateValid(key):
    N = len(key)

    for i in key:
        if i < 0 or i > 26:
            return False
    return True


def score_sentence(key, scores_dp, sentence):
    # if this score has already been calculated, just return it
    if key in scores_dp:
        return scores_dp[key]

    # else, calculate the score and return it
    dcr_sentence = part1.encryptBlock(sentence, key, False)  # from part 1
    return part2.get_ptb_sentence_score(dcr_sentence, ptb_prob_weights)  # from part 2


def score_key(key, scores_dp, sentence):
    # if this score has already been calculated, just return it
    if key in scores_dp:
        return scores_dp[key]

    # apply key to sentence
    sent = part1.encryptBlock(sentence, key, True)

    # calculate score from how well the individual character frequencies match up
    base_freq = part2.get_ptb_ngrams()[0]
    sent_freq = {}
    for c in sent:
        if c in sent_freq:
            sent_freq[c] += 1
        else:
            sent_freq[c] = 1

    base_sum = sum(base_freq.values())
    sent_sum = len(sent)
    base_prob = {c: v / base_sum for c, v in base_freq.items()}
    sent_prob = {c: v / sent_sum for c, v in sent_freq.items()}

    # compare base_freq and sent_freq
    # positive score is good
    score = 0
    for c in base_prob:
        # doesn't even exist
        if c not in sent_prob:
            score -= base_prob[c]
        else:
            score -= math.fabs(base_prob[c] - sent_prob[c])

    return score


def simulated_annealing(get_score, get_neighbour, sentence, curr_key, score_scale, max_steps=MAX_STEPS):
    temperature = MAX_TEMPERATURE
    # track score over time
    scores_dp = OrderedDict()

    # keep the best resolution for printing at the end
    best_score = get_score(curr_key, scores_dp, sentence)
    best_key = curr_key
    # best_decrypt = part1.encryptBlock(sentence, list(best_key), False)
    step = 0
    while step < max_steps:
        # score current state (only care about maximum per location)
        curr_score = get_score(curr_key, scores_dp, sentence)
        # track score
        scores_dp[curr_key] = curr_score
        # print(temperature, curr_score)

        # pick random neighbour
        new_key = get_neighbour(curr_key, isStateValid)
        new_score = get_score(new_key, scores_dp, sentence)

        # export for visualization
        # print("{}|{}|{}".format(time.time(), best_score, best_decrypt), file="visual_output.txt")

        if pick_state(curr_score, new_score, temperature, MAX_TEMPERATURE, BASE_SELECTIVITY,
                      score_scale) > random.random():
            curr_key = new_key
            if new_score > best_score:
                best_score = new_score
                best_key = new_key

        # print("step {} \tbest {}".format(step, best_score))

        temperature = anneal(temperature, step)
        step += 1

    return best_key, best_score


def crack3b(ciphertext):
    ciphertext = [text.strip() for text in ciphertext.split("|")]
    # parse the input
    orig_sentence = ciphertext[1]
    sentence = part2.sanitize_input(orig_sentence)

    key_length = int(ciphertext[0])

    best_key = None
    best_score = None

    for seed in range(60):
        random.seed(seed)
        curr_key = tuple(random.randint(0, 26) for _ in range(key_length))
        curr_key, key_score = simulated_annealing(score_key, get_neighbour_block_key, sentence, curr_key, 20)
        key, score = simulated_annealing(score_sentence, get_neighbour_block_key, sentence, curr_key, 0.1)

        if best_score is None or score > best_score:
            best_score = score
            best_key = key

    print("best score (annealing): {}".format(best_score))
    # print("best score: {}".format(max(max(arr) for arr in arrays)))
    print("best key: {}".format(best_key))
    print(part1.encryptBlock(sentence, list(best_key), False))
    return " ".join([" ".join((str(k) for k in best_key)), "|", part1.encryptBlock(orig_sentence, best_key, False)])


def crack3c(orig_sentence):
    sentence = part2.sanitize_input(orig_sentence)

    best_key = None
    best_score = None

    for key_length in range(1, 8):
        for seed in range(20):
            random.seed(seed)
            curr_key = tuple(random.randint(0, 26) for _ in range(key_length))
            curr_key, key_score = simulated_annealing(score_key, get_neighbour_block_key, sentence, curr_key, 20,
                                                      MAX_STEPS / 4)
            key, score = simulated_annealing(score_sentence, get_neighbour_block_key, sentence, curr_key, 0.1,
                                             MAX_STEPS / 4)

            if best_score is None or score > best_score:
                best_score = score
                best_key = key

    print("best score (annealing): {}".format(best_score))
    # print("best score: {}".format(max(max(arr) for arr in arrays)))
    print("best key: {}".format(best_key))
    print(part1.encryptBlock(sentence, list(best_key), False))
    return " ".join([" ".join((str(k) for k in best_key)), "|", part1.encryptBlock(orig_sentence, best_key, False)])


def main():
    doPart("3a", crack3a)
    doPart("3b", crack3b)
    doPart("3c", crack3c)


if __name__ == "__main__":
    main()
