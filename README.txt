########################################################################
############            twitter_geolocation             ################
########################################################################

========================================================================
location.py
  - extracts user profile location tag from an input
  - usage: location.py [options]

    options:
        -h, --help              show this help message and exit
        -v, --verbose           turn on verbose mode
        -f FILE, --file=FILE    input file to search
        - o OUTPUT_FILE, --outfile=OUTPUT_FILE
                                file to write output of location search
  - from location import loc
        loc(contents)           # contents: text to search

========================================================================
crawler.py
  - crawls through user pages in a given directory, using location.py 
    to extract location data
  - usage: crawler.py [options]

    options:
        -h, --help               show this help message and exit
        -v, --verbose            turn on verbose mode
        -s DIR, --source=DIR     directory to find user pages in
        -f FILE, --file=FILE     file to write user page names to
        -o OUTPUT_FILE, --outfile=OUTPUT_FILE
                                 file to write output of location data
                                 extracted by crawl
