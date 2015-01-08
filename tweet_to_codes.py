import re
import numpy as np

codes = np.genfromtxt('just_the_codes.txt', dtype=str)

print codes


def tweet_to_codes(tweet):
    out = []
    words = re.findall(r"[\w']+", tweet)

    for i in words:
        if i in codes:
            out.append(i)

#    print h

    return out

if __name__ == "__main__":

    tweet_to_codes('this is an example of a tweet #ORD #BOS sea-lax')

    print out
