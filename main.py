#!/usr/bin/env python3
from parsers.JsonMessageParser import JsonMessageParser
from wordclouds.WordCloudGenerator import WordCloudGenerator
import os

# from IPython import embed; embed() # TODO remove after done debugging
# import datetime, json
# import threading, urllib2, time
# import numpy as np
# import sys, os, IPython, httplib


# Input/output filepaths
INPUT_DIRECTORY = "input/"
OUTPUT_DIRECTORY = "output/"


class GroupchatAnalyzer:
    def __init__(self):
        return

    def run_main(self):
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)

        print("Parsing messages...")
        self.messages, self.participants = JsonMessageParser(INPUT_DIRECTORY).parse_message_data()
        print("Found " + str(len(self.messages)) + " messages, ", str(len(self.participants)) + " participants")

        print("Generating word clouds...")
        WordCloudGenerator(OUTPUT_DIRECTORY).generate_wordclouds(self.messages)
        print("Done generating word clouds")



# Main
if __name__ == "__main__":
    GroupchatAnalyzer().run_main()
