#!/usr/bin/env python3
from __future__ import division
# import numpy as np
# import sys, os, IPython, httplib
from IPython import embed # TODO remove after done debugging
# import datetime, json
# import threading, urllib2, time
from parsers.JsonMessageParser import JsonMessageParser


class GroupchatAnalyzer:
    def __init__(self):
        self.messages, self.participants = JsonMessageParser().parse_message_data()
        return

    def run_main(self):
    	print(str(len(self.messages)) + " messages, ", str(len(self.participants)) + " participants")
    	return


# Main
if __name__ == "__main__":
    GroupchatAnalyzer().run_main()

