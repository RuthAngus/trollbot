import numpy as np
import requests
import json
from requests_oauthlib import OAuth1
import time
import tweepy
from emissions import airports_to_co2
from tweet_to_codes import tweet_to_codes
import ConfigParser
from nomad import nomad_finder

# Twitter API settings.
url = "https://stream.twitter.com/1.1/statuses/filter.json"
client_key, client_secret, user_key, user_secret = \
        np.genfromtxt("keys.txt", skip_header=1, dtype=str).T

def monitor(params):
    wait = 0
    auth = OAuth1(client_key, client_secret, user_key, user_secret)
    while 1:
        try:
            try:
                r = requests.post(url, data=params, auth=auth, stream=True,
                                 timeout=90)

            except requests.exceptions.ConnectionError:
                print("request failed.")
                wait = min(wait + 0.25, 16)

            else:
                code = r.status_code
                print("{0} returned: {1}".format(url, code))
                if code == 200:
                    wait = 0
                    try:
                        for line in r.iter_lines():
                            if line:
                                yield json.loads(line)

                    except requests.exceptions.Timeout:
                        print("request timed out.")

                    except Exception as e:
                        print("failed with {0}".format(e))

                elif code == 420:
                    if wait == 0:
                        wait = 60

                    else:
                        wait *= 2

                elif code in [401, 403, 404, 500]:
                    if wait == 0:
                        wait = 5

                    else:
                        wait = min(wait * 2, 320)

                else:
                    r.raise_for_status()

        except KeyboardInterrupt:
            print("Exiting.")
            break

        time.sleep(wait)

def tweet(emission, codes, handle):

    config = ConfigParser.ConfigParser()
    sect = "twitter"

    print("Posting to twitter...")
    auth = tweepy.OAuthHandler(client_key, client_secret)
    auth.set_access_token(user_key, user_secret)
    api = tweepy.API(auth)

    sent = "@%s I hear you're flying between %s and %s. Your carbon emissions will be %s Kg." \
            % (handle, codes[0], codes[1], int(emission))
    print sent

#     time.sleep(5*60)
    api.update_status(sent)

def nomad_tweet():
    config = ConfigParser.ConfigParser()
    sect = "twitter"
    print("Posting to twitter...")
    auth = tweepy.OAuthHandler(client_key, client_secret)
    auth.set_access_token(user_key, user_secret)
    api = tweepy.API(auth)
    trolls = np.genfromtxt("trollolol.txt", dtype=str)
    sent = "%s" % trolls[np.randint(0, len(trolls))]
    print sent
#     time.sleep(5*60)
    api.update_status(sent)

if __name__ == "__main__":

    iapa = np.genfromtxt("just_the_codes.txt", dtype=str).T
    params = {"track": iapa[:100]}

    sv = open("text.txt", 'w')
    for o in monitor(params):
        text = o["text"]
        handle = o.get("user", {}).get("screen_name", None)
#         if o.get("lang", None) == "en":
        if nomad_finder(text) == True:
            nomad_tweet()

        codes = tweet_to_codes(text)

        if len(codes) == 2 and codes[0] != codes[1]:
            emission = airports_to_co2(codes[0], codes[1])

            if emission > 0:
                print text
                print codes
                print emission

                tweet(emission, codes, handle)
        sv.write(text.encode('ascii', 'ignore') + '\n')
