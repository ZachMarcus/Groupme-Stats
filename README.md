# GroupMe-stats

Basic script to analyze our groupme chat



Requirements:

 - Python Modules
    pip3 install requirements.txt

 - GroupMe API key

Login to 
    https://dev.groupme.com/session/new
Grab an API key from the Access Token on the upper right

It should be run like so:

    python3 testGroupMe.py --help

For those in the Bio/ECE fam, first download all the messages using

    python3 testGroupMe.py --apiKey=<apiKey> --groupName="Bio/ECE fam" --messageToFile=out.json

There may be some duplicates, so see the analysis script for the fix.

The class that contains everything and does the modifications is in GroupMe.py
The script that does the argument parsing and decision making is testGroupMe.py

The class has a method at the bottom that should be modified to do whatever analysis you like.

