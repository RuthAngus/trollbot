import re
import numpy as np

codes = np.genfromtxt('just_the_codes.txt', dtype=str)

print codes


def tweet_to_codes(tweet):
    out = []
    words = re.findall(r"[\w']+", tweet)

    for i in xrange(1, len(words)):
        if (words[i-1] in codes) and (words[i] in codes):
            out.append(words[i-1])
            out.append(words[i])

#    print h

    return out

if __name__ == "__main__":

    out = tweet_to_codes('this is an example of an LHR->MDW tweet #ORD #BOS sea-lax')

    print out
