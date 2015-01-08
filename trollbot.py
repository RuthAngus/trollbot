import numpy as np
import requests
import json
from requests_oauthlib import OAuth1
import time
import tweepy
from emissions import airports_to_co2
from tweet_to_codes import tweet_to_codes

# Twitter API settings.
url = "https://stream.twitter.com/1.1/statuses/filter.json"
client_key, client_secret, user_key, user_secret = \
        np.genfromtxt("keys.txt", skip_header=1, dtype=str).T

iapa = np.genfromtxt("just_the_codes.txt", dtype=str).T
params = {"track": iapa[:100]}

def monitor():
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

def tweet(emission):

    config = ConfigParser.ConfigParser()
    config.read("local.cfg")
    sect = "twitter"

    print("Posting to twitter...")
    auth = tweepy.OAuthHandler(config.get(sect, "consumer_key"),
                               config.get(sect, "consumer_secret"))
    auth.set_access_token(config.get(sect, "user_key"),
                          config.get(sect, "user_secret"))
    api = tweepy.API(auth)

    sent = "Your total carbon emissions are %s Kg"
    api.update_status(sent)

if __name__ == "__main__":

    for o in monitor():
        text = o["text"]
        print text
        codes = tweet_to_codes(text)
        print codes
        emission = airports_to_co2(codes[0], codes[1])
        print emission

#         tweet(emission)
        raw_input('enter')
