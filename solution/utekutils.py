"""Common constants and helper functions shared between solutions.
"""

"""Constant for the ASCII code of uppercase A."""
asciiForA = 0x41
"""Constant for the ASCII code of uppercase Z."""
asciiForZ = 0x5a
"""The hardcoded lambda values for part 3."""
ptb_prob_weights = [1e-5,1e-4,1e-3,1e-2,1e-1,0.88889]


def doPart(infilename, partfn):
    """Run partfn on each line of the problem input file, and write the return value to the problem output file.
    Args:
        infilename (str): The problem name (e.g. 1a)
        partfn (func(str) -> object): The solution function taking in a line from infile and returning an object to print to outfile.
    """
    with open("../input/" + infilename + ".in", "r") as infile, open("../output/" + infilename + ".out",
                                                                     "w") as outfile:
        for l in infile:
            print(partfn(l.rstrip("\n")), file=outfile)
