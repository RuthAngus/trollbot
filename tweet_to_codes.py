import re
import numpy as np

codes = np.genfromtxt('just_the_codes.txt', dtype=str)

#print codes


def tweet_to_codes(tweet):
    out = []
    tweet = tweet.replace(';', '')
    tweet = tweet.replace('&gt', '>')
  #  words = re.findall(r"[\w']+", tweet)
    tweet = tweet.replace(' -> ', '->')
   # tweet = tweet.replace(' - ', '-')


    words1 = re.findall(r"([a-zA-Z]{3}->[a-zA-Z]{3})", tweet)
    words2 = re.findall(r"([a-zA-Z]{3}-[a-zA-Z]{3})", tweet)

    words = words1 + words2

    try:
        for i in xrange(len(words)):
            words_sh = words[i].replace('>','').split('-')

            for j in xrange(1, len(words_sh)):
                if (words_sh[i-1] in codes) and (words_sh[i] in codes):
                    out.append(words_sh[i-1])
                    out.append(words_sh[i])
    except:
        pass


  #  for i in xrange(1, len(words)):
  #      if (words[i-1] in codes) and (words[i] in codes):
  #          out.append(words[i-1])
  #          out.append(words[i])

#    print h

    return out

if __name__ == "__main__":

    out = tweet_to_codes('this is an example of an LHR -> MDW tweet #ORD #BOS SEA - LAX')

    print out
