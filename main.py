#!/usr/bin/env python3
from parsers.JsonMessageParser import JsonMessageParser
from wordclouds.WordCloudGenerator import WordCloudGenerator
from messagestats.AggregatedMessageAnalyzer import AggregatedMessageAnalyzer
from graphers.BarGraphsGenerator import BarGraphsGenerator
from graphers.TimeSeriesGenerator import TimeSeriesGenerator
import os
# from IPython import embed; embed(); import sys; sys.exit(0) # For debugging


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

        print("Generating statistics...")
        AggregatedMessageAnalyzer(OUTPUT_DIRECTORY).generate_stats(self.messages, self.participants)

        print("Generating bar graphs...")
        BarGraphsGenerator(OUTPUT_DIRECTORY).generate_graphs(self.messages)

        print("Generating time series graphs...")
        TimeSeriesGenerator(OUTPUT_DIRECTORY).generate_graphs(self.messages)

        print("Generating word clouds...")
        WordCloudGenerator(OUTPUT_DIRECTORY).generate_wordclouds(self.messages)
        print("Done generating word clouds")



# Main
if __name__ == "__main__":
    GroupchatAnalyzer().run_main()
