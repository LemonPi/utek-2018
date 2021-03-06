import re
import pickle
import math
from utekutils import ptb_prob_weights, doPart, inf

_SANITIZE_INPUT_RE = re.compile(r'<unk>|[^\w]')
_SANITIZE_WITHOUT_SPACE_RE = re.compile(r'<unk>|N|[^\w]')
_SANITIZE_WITH_SPACE_RE = re.compile(r'<unk>|N|[^\w] ')


def sanitize_input(text):
    return _SANITIZE_INPUT_RE.sub('', text).upper()


def sanitize_without_space(text):
    return _SANITIZE_WITHOUT_SPACE_RE.sub('', text).upper()


def sanitize_with_spaces(text):
    return _SANITIZE_WITH_SPACE_RE.sub('', text).upper()


def build_ngram_from_corpus(ngrams, corpus, maxn):
    for i in range(len(corpus)):
        for n in range(maxn):  # actually n+1 gram since index from 0
            if i + n == len(corpus):
                break

            ngram = corpus[i:i + n + 1]
            if ngram in ngrams[n]:
                ngrams[n][ngram] += 1
            else:
                ngrams[n][ngram] = 1


def count_chars(corpus, maxn):
    # 2a and for everything else
    # remove all <unk>, N, non-alphabetic
    corpus = sanitize_without_space(corpus)
    ngrams = [{} for _ in range(1, maxn + 1)]

    build_ngram_from_corpus(ngrams, corpus, maxn)
    return ngrams


def count_chars_in_words(corpus, maxn):
    # split along all whitespace
    corpus = sanitize_with_spaces(corpus).split()
    ngrams = [{} for _ in range(1, maxn + 1)]

    for word in corpus:
        build_ngram_from_corpus(ngrams, word, maxn)

    return ngrams


MAX_N = 7
PTB_SRC = "../ptb.train.txt"

ptb_ngrams = None
ptb_ngrams_in_words = None


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
            with open(PTB_P, 'wb') as dump:
                pickle.dump(ngrams, dump)

    ptb_ngrams = ngrams
    return ngrams


def get_ptb_ngrams_chars_in_words():
    global ptb_ngrams_in_words
    if ptb_ngrams_in_words:
        return ptb_ngrams_in_words

    PTB_P = "ptb_chars_in_words.p"
    try:
        ngrams = pickle.load(open(PTB_P, "rb"))
    except FileNotFoundError:
        with open(PTB_SRC, 'r') as text:
            ngrams = count_chars_in_words(text.read(), MAX_N)
            with open(PTB_P, 'wb') as dump:
                pickle.dump(ngrams, dump)

    ptb_ngrams_in_words = ngrams
    return ngrams


def get_count(ngrams, word):
    ngram = ngrams[len(word) - 1]
    if word not in ngram:
        return 0
    else:
        return ngram[word]


def get_ptb_sentence_score(sentence, weights, ngrams=None):
    # assumes sentence is sanitized
    # split sentence into MAX_N grams and take the sum of the log prob
    prob = 0
    for i in range(max(1, len(sentence) - MAX_N + 1)):
        word = sentence[i:i + MAX_N]
        # print("{}: {}".format(i, word))
        p = get_ptb_prob(word, weights, ngrams)
        # print("logp: {}".format(p))
        # compare against 0
        if abs(p) > 1e-7:
            prob += math.log(p)
        else:
            prob -= 50

    # print("sent {}".format(prob))

    return prob


def get_ptb_prob(word, weights, ngrams=None):
    if ngrams is None:
        ngrams = get_ptb_ngrams()
    prob = 0
    for i in range(1, len(word)):
        denom = get_count(ngrams, word[:i])
        num = get_count(ngrams, word[:i + 1])
        # print("{}:{}\t{}:{}".format(word[:i + 1], num, word[:i], denom))

        # anything else will also be 0
        if denom == 0:
            break

        prob += weights[i - 1] * num / denom

    return prob


def part_2a(line):
    line = [side.strip() for side in line.split("|")]
    corpus = line[0]
    word = sanitize_input(line[1])

    # print("[{}] [{}]".format(corpus, word))

    if corpus == "PTB":
        ngrams = get_ptb_ngrams()
        # ngrams = get_ptb_ngrams_chars_in_words()
    else:
        ngrams = count_chars(corpus, MAX_N)

    # print(get_count(ngrams, word))
    return get_count(ngrams, word)


def part_2b(line):
    line = [sanitize_input(sent.strip()) for sent in line.split("|")]
    most_likely_prob = -inf
    most_likely_sentence = None

    for i in range(len(line)):
        sentence = line[i]
        logp = get_ptb_sentence_score(sentence, ptb_prob_weights)
        print("---\n{}:{}\n".format(sentence, logp))
        if logp > most_likely_prob:
            most_likely_prob = logp
            most_likely_sentence = i + 1

    return most_likely_sentence


def main():
    doPart("2a", part_2a)
    doPart("2b", part_2b)


if __name__ == "__main__":
    main()
