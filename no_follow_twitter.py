
"""
3 – View who doesn’t follow you (Python)

Some people don’t like the idea of following people who don’t follow you back. If you recognized yourself in this statement, 
there’s a huge amount of chances that you’ll enjoy the following Python code snippet.
Simply type your Twitter username and password on line 4 and call the file using the Python interpreter.
Source : http://blog.davidziegler.net/post/107429458/see-which-twitterers-don-t-follow-you-back-in-less-than

"""

import twitter, sys, getpass, os

def call_api(username,password):
    api = twitter.Api(username,password)
    friends = api.GetFriends()
    followers = api.GetFollowers()
    heathens = filter(lambda x: x not in followers,friends)
    print "There are %i people you follow who do not follow you:" % len(heathens)
    for heathen in heathens:
        print heathen.screen_name
        
if __name__ == "__main__":
    password = getpass.getpass()
    call_api(sys.argv[1], password)

