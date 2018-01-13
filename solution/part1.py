asciiForA = 0x41
asciiForZ = 0x5a
def encryptMap(intext, strMap, encrypting):
    outstr = []
    if not encrypting:
        newStrMap = [" "]*26
        for i in range(len(strMap)):
            newStrMap[ord(strMap[i]) - asciiForA] = chr(i + asciiForA)
        strMap = "".join(newStrMap)
            
    for a in intext:
        charCode = ord(a)
        if charCode >= asciiForA and charCode <= asciiForZ:
            outchar = strMap[ord(a) - asciiForA]
        else:
            outchar = a
        outstr.append(outchar)
    return "".join(outstr)

def encryptBlock(intext, key, encrypting):
    outstr = []
    keyIndex = 0
    for i in range(len(intext)):
        inchar = intext[i]
        charCode = ord(inchar)
        if charCode >= asciiForA and charCode <= asciiForZ:
            addend = key[keyIndex]
            if not encrypting:
                addend = -1 * addend
            keyIndex = (keyIndex + 1) % len(key)
            outchar = chr(asciiForA + ((charCode - asciiForA + addend) % 26))
        else:
            outchar = inchar
        outstr.append(outchar)
    return "".join(outstr)

def part1(instr, partname):
    parts = instr.split(" | ")
    encrypting = parts[0] == "ENCRYPT"
    if partname == "1c":
        result = encryptMap(parts[2], parts[1], encrypting)
    else:
        result = encryptBlock(parts[2], [int(a) for a in parts[1].split()], encrypting)
    return result

def part1file(infilename):
    with open("input/" + infilename + ".in", "r") as infile, open("output/" + infilename + ".out", "w") as outfile:
        for l in infile:
            print(part1(l.rstrip("\n"), infilename), file=outfile)

def main():
    part1file("1a")
    part1file("1b")
    part1file("1c")

if __name__ == "__main__":
    main()