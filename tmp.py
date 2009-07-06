#!/usr/bin/env python

from tweets import findTweets

def main():
    twt1 = "blah blah blah \"status_01234\" something something <span class=\"entry-content\">this is my tweet!</span><span entry=\"meta entry-meta\">other stuff here blah blah blah <span class=\"published\" title=\"2009-07-02T00:00:00\""
    twt2 = "blah blah blah \"status_56789\" something something <span class=\"entry-content\">a second tweet!</span><span entry=\"meta entry-meta\">other stuff here blah blah blah <span class=\"published\" title=\"2009-07-02T00:00:00\""
    tmp = twt1 + twt2
    tweets = findTweets(tmp)
    print tweets

if __name__ == "__main__":
    main()
