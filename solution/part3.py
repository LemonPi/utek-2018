import part1
import part2
from utekutils import doPart, asciiForA, asciiForZ, ptb_prob_weights, inf

def crack3a(ciphertext):
    bestScore = -inf
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

def main():
    doPart("3a", crack3a)

if __name__ == "__main__":
    main()
