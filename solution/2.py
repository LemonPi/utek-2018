import re
import pickle
import math


def sanitize_input(text):
    return re.sub(r'<unk>|[^\w]', '', text).upper()


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


def get_count(ngrams, word):
    ngram = ngrams[len(word) - 1]
    if word not in ngram:
        return 0
    else:
        return ngram[word]


def get_ptb_sentence_score(sentence, weights):
    # assumes sentence is sanitized
    # split sentence into MAX_N grams and take the sum of the log prob
    prob = 0
    for i in range(len(sentence) - MAX_N + 1):
        word = sentence[i:i + MAX_N]
        print("{}: {}".format(i, word))
        p = get_ptb_prob(word, weights)
        print("logp: {}".format(p))
        if p != 0:
            prob += math.log(p)

    return prob


def get_ptb_prob(word, weights):
    ngrams = get_ptb_ngrams()
    prob = 0
    for i in range(1, len(word)):
        denom = get_count(ngrams, word[:i])
        num = get_count(ngrams, word[:i + 1])
        print("{}:{}\t{}:{}".format(word[:i + 1], num, word[:i], denom))

        # anything else will also be 0
        if denom == 0:
            break

        prob += weights[i] * num / denom

    return prob


def part_2a(line, output):
    line = [side.strip() for side in line.split("|")]
    corpus = line[0]
    word = sanitize_input(line[1])

    print("[{}] [{}]".format(corpus, word))

    if corpus == "PTB":
        ngrams = get_ptb_ngrams()
    else:
        ngrams = count_chars(corpus, MAX_N)

    print(get_count(ngrams, word))
    print(get_count(ngrams, word), file=output)


def part_2b(line, output):
    line = [sanitize_input(sent.strip()) for sent in line.split("|")]
    most_likely_prob = -math.inf
    most_likely_sentence = None

    WEIGHTS = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.888889]

    for i in range(len(line)):
        sentence = line[i]
        logp = get_ptb_sentence_score(sentence, WEIGHTS)
        print("---\n{}:{}\n".format(sentence, logp))
        if logp > most_likely_prob:
            most_likely_prob = logp
            most_likely_sentence = i + 1

    print(most_likely_sentence, file=output)


def do_part_2a():
    with open("../input/2a.in", 'r') as input:
        with open("../output/2a.out", 'w') as output:
            for line in input:
                part_2a(line, output)


def do_part_2b():
    with open("../input/2b.in", 'r') as input:
        with open("../output/2b.out", 'w') as output:
            for line in input:
                part_2b(line, output)


if __name__ == "__main__":
    # do_part_2a()
    do_part_2b()
