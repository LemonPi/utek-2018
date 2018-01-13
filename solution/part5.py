import part2
import part3
from utekutils import doPart, asciiForA, asciiForZ, ptb_prob_weights, inf
from math import exp
import random

# https://stackoverflow.com/a/14992648
def weighted_random(rand, pairs):
    # normalize weights to 1
    summed = sum(a[0] for a in pairs)
    if summed == 0:
        return pairs[0][1]
    r = rand.random()
    #print(r)
    for (weight, value) in pairs:
        r -= weight / summed
        if r <= 0: return value
    return pairs[-1][1]
    
SEED = 1234
TRIES_PER_SENTENCE = 1
def gen5(curStr):
    bestScore = -inf
    bestSentence = None
    for i in range(TRIES_PER_SENTENCE):
        newSentence = genRandSentence(curStr, SEED + i)
        newScore = part2.get_ptb_sentence_score(part2.sanitize_input(newSentence), ptb_prob_weights)
        if newScore > bestScore:
            bestSentence = newSentence
            bestScore = newScore
    #print(bestSentence)
    return bestSentence

def getWeight(word):
    weights = ptb_prob_weights
    # Reversed version of get_ptb_sentence_score taking into account the last n-grams instead of the first n-grams
    # ie. Pr(ABCD) = lambda1*count(CD)/count(C) + lambda2*count(BCD)/count(BC)
    ngrams = part2.get_ptb_ngrams()
    prob = 0
    for i in range(1, len(word)):
        denom = part2.get_count(ngrams, word[i:])
        num = part2.get_count(ngrams, word[i-1:])
        if False:
            print("{}:{}\t{}:{}".format(word[i-1:], num, word[i:], denom))

        # anything else will also be 0
        if denom == 0:
            break

        prob += weights[i - 1] * num / denom

    return prob

def genRandSentence(curStr, seed):
    rand = random.Random(seed)
    #curSentenceScore = part2.get_ptb_sentence_score(part2.sanitize_input(curStr), ptb_prob_weights)
    for i in range(1000):
        weights = []
        for newCharCode in range(asciiForA, asciiForZ + 1):
            newStr = curStr + chr(newCharCode)
            # Note that get_ptb_sentence_score loops through the sentence, and for each index it calculates ngrams for (i, i+7)
            # and then sum the score
            # and only the last ngram calculated should differ between all these sentences
            # since only the last letter is changed
            # so we can optimize the score calculation by reusing the old sentence score
            newStrEnd = part2.sanitize_input(newStr)[-part2.MAX_N:]
            #print(i, newStrEnd)
            #newScore = part2.get_ptb_sentence_score(newStrEnd, ptb_prob_weights) + curSentenceScore
            #newWeight = exp(newScore)
            #print(newStr)
            newWeight = getWeight(newStrEnd)
            weights.append((newWeight**2, newStr))
        #bloop = [str(a[0]) + ":" + a[1][0][-1] for a in sorted(weights, key=lambda a: a[0], reverse=True)]
        #print(bloop)
        curStr = weighted_random(rand, weights)
        #print(curStr, curSentenceScore)
    #print(curStr)
    return curStr

def main():
    doPart("5a", gen5)

if __name__ == "__main__":
    main()