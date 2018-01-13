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

def part1(instr):
    parts = instr.split(" | ")
    encrypting = parts[0] == "ENCRYPT"
    if len(parts[1]) == 26 and parts[1].isalpha():
        result = encryptMap(parts[2], parts[1], encrypting)
    else:
        result = encryptBlock(parts[2], [int(a) for a in parts[1].split()], encrypting)
    print(result)

if __name__ == "__main__":
    with open("../input/1b.in", "r") as infile:
        for l in infile:
            part1(l.rstrip("\n"))