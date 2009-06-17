########################################################################
############            twitter_geolocation             ################
########################################################################

========================================================================
location.py
  - extracts user profile location tag from an input

  - usage: location.py [options]

    options:

        -h, --help              show this help message and exit
        -f FILE, --file=FILE    input file to search
        -o OUTPUT_FILE, --outfile=OUTPUT_FILE
                                file to write output of location search
        -s, --stdout            use standard output instead of file
        -v, --verbose           turn on verbose mode

  - from location import loc, ltweet
    contents = "string to search"
    loc(contents)               # returns address:coordinates pair
    ltweet(contents)            # returns instances of l:____ matches

========================================================================
crawler.py
  - crawls through user pages in a given directory, using location.py 
    to extract location data

  - usage: crawler.py [options]

    options:

        -h, --help               show this help message and exit
        -d DIR, --directory=DIR  directory to find user pages in
        -f ONLY_FILE, --file=ONLY_FILE
                                 single file in directory to run
        -m, --no-metacarta       do not process location information in
	                         profile using MetaCarta
        -o OUTPUT_FILE, --outfile=OUTPUT_FILE
                                 file to write output of location data
                                 extracted by crawl
        -s, --stdout             use standard output instead of file
        -t, --no-tweets          do not process l:____ matches found in
                                 user tweets
        -u USER_FILE, --ufile=USER_FILE
                                 file to write user page names to
        -v, --verbose            turn on verbose mode

  - from crawler import tattrs
    tattrs(tweet)                #returns statusID:timestamp pair
    meta(address)                #returns number of location matches,
                                 #  top match, error flag (for login)

========================================================================
mapUsers.py
  - crawls through data output from crawler.py and generates HTML and
    PHP files to display a map of users using the Google Map API

  - usage: mapUsers.py [options]

      -h, --help                 show this help message and exit
      -d DIR, --directory=DIR    directory to find user data in
      -f FILE, --file=FILE       single file in directory to run
      -m FILE, --mapfile=FILE    file to write map content to
      -s, --stdout               use standard output instead of output
                                 file
      -t FILE, --topfile=FILE    file to write opening html tags and
                                 javascript to
      -u FILE, --ufile=FILE      file to write user data names to
      -v, --verbose              turn on verbose mode
