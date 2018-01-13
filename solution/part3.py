import part1
import part2

def crack3a(instr):
    parts = instr.split(" | ")
    ciphertext = parts[0]
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

def part3a():
    infilename = "3a"
    with open("input/" + infilename + ".in", "r") as infile, open("output/" + infilename + ".out", "w") as outfile:
        for l in infile:
            print(crack3a(l.rstrip("\n")), file=outfile)

def main():
    part3a()
if __name__ == "__main__":
    main()