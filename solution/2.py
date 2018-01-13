import re
import pickle


def sanitize_without_space(text):
    return re.sub(r'<unk>|N|[^\w]', '', text).upper()


def count_chars(corpus, maxn):
    # 2a and for everything else
    # remove all <unk>, N, non-alphabetic
    corpus = sanitize_without_space(corpus)
    ngrams = [{} for _ in range(1, maxn + 1)]

    for i in range(len(corpus)):
        for n in range(maxn):  # actually n+1 gram since index from 0
            if i + n == len(corpus):
                break

            ngram = corpus[i:i + n + 1]
            if ngram in ngrams[n]:
                ngrams[n][ngram] += 1
            else:
                ngrams[n][ngram] = 1

    return ngrams


MAX_N = 7
PTB_SRC = "../ptb.train.txt"


ptb_ngrams = None
def get_ptb_ngrams():
    global ptb_ngrams
    if ptb_ngrams:
        return ptb_ngrams

    PTB_P = "ptb.p"
    try:
        ngrams = pickle.load(open(PTB_P, "rb"))
    except FileNotFoundError:
        with open(PTB_SRC, 'r') as text:
            ngrams = count_chars(text.read(), MAX_N)
            with open('wb') as dump:
                pickle.dump(ngrams, dump)

    ptb_ngrams = ngrams
    return ngrams


def get_prob(ngrams, word):
    ngram = ngrams[len(word) - 1]
    if word not in ngram:
        return 0
    else:
        return ngram[word]


def part_2a(line, output):
    line = [side.strip() for side in line.split("|")]
    corpus = line[0]
    word = re.sub(r'<unk>|[^\w]', '', line[1])

    print("[{}] [{}]".format(corpus, word))

    if corpus == "PTB":
        ngrams = get_ptb_ngrams()
    else:
        ngrams = count_chars(corpus, MAX_N)

    print(get_prob(ngrams, word))
    print(get_prob(ngrams, word), file=output)


def get_ptb_prob(string):
    return 0


# with open(PTB_SRC, 'r') as src:
#     # print(sanitize_without_space(src.read()))
#     ngrams = get_ptb_ngrams()
if __name__ == "__main__":
    with open("../input/2a.in", 'r') as input:
        with open("../output/2a.out", 'w') as output:
            for line in input:
                print(line)
                part_2a(line, output)
