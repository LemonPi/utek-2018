import part1
import part2

asciiForA = 0x41
asciiForZ = 0x5a

def crack3a(ciphertext):
    bestScore = -1
    bestText = None
    bestKey = -1
    for i in range(0, 26):
        newText = part1.encryptBlock(ciphertext, [i], False)
        newScore = part2.get_ptb_prob(newText)
        if newScore > bestScore:
            bestScore = newScore
            bestText = newText
            bestKey = i
    return str(bestKey) + " | " + bestText

def doPart(infilename, partfn):
    with open("input/" + infilename + ".in", "r") as infile, open("output/" + infilename + ".out", "w") as outfile:
        for l in infile:
            print(partfn(l.rstrip("\n")), file=outfile)

def main():
    doPart("3a", crack3a)

if __name__ == "__main__":
    main()