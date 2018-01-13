from utekutils import doPart

"""Solution for Part 1 (encrypting and decrypting) of the UTEK 2018 competition.
"""

"""Constant for the ASCII code of uppercase A."""
asciiForA = 0x41
"""Constant for the ASCII code of uppercase Z."""
asciiForZ = 0x5a

def encryptMap(intext, strMap, encrypting):
    """Encrypt/decrypt an input text using a letter mapping and return the result as a string.
    Args:
        intext (str): The string to encrypt or decrypt.
        strMap (str): The alphabet mapping from the plaintext to the ciphertext.
        encrypting (bool): True if encrypting intext, False if decrypting.
    Returns:
        str: the encrypted/decrypted string.
    """
    outstr = []
    if not encrypting:
        # Invert the mapping.
        # Then decryption is equal to applying the inverted mapping as an encryption.
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
    """Encrypt/decrypt an input text using a block-based modified Caesar cipher and return the result as a string.
    Args:
        intext (str): The string to encrypt or decrypt.
        key (array): An array of ints specifying the increment in the Caesar cipher for each position in the cipher block.
        encrypting (bool): True if encrypting intext, False if decrypting.
    Returns:
        str: the encrypted/decrypted string.
    """
    outstr = []
    keyIndex = 0
    for i in range(len(intext)):
        inchar = intext[i]
        charCode = ord(inchar)
        if charCode >= asciiForA and charCode <= asciiForZ:
            addend = key[keyIndex]
            if not encrypting:
                # Decryption of a Caesar cipher requires one to subtract instead of add the key value to the input.
                addend = -1 * addend
            keyIndex = (keyIndex + 1) % len(key)
            outchar = chr(asciiForA + ((charCode - asciiForA + addend) % 26))
        else:
            outchar = inchar
        outstr.append(outchar)
    return "".join(outstr)

def part1(instr, partname):
    """Solve one line of an input file of part 1.
    """
    parts = instr.split(" | ")
    encrypting = parts[0] == "ENCRYPT"
    if partname == "1c":
        result = encryptMap(parts[2], parts[1], encrypting)
    else:
        result = encryptBlock(parts[2], [int(a) for a in parts[1].split()], encrypting)
    return result

def main():
    """Run the solution to part 1.
    """
    for part in ["1a", "1b", "1c"]:
        doPart(part, lambda instr: part1(instr, part))

if __name__ == "__main__":
    main()