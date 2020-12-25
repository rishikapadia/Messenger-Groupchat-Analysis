from datetime import datetime
from collections import Counter
import os


OUTPUT_DIRECTORY = "graphs/"
OUTPUT_FILE_FORMAT = ".png"

# JSON field names
MESSAGE_CONTENT = "content"


class TimeSeriesGenerator:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        return


    def generate_graphs(self, messages):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

        # Time series:
        # - Time series of messages (bucket size = 1 month? window-size averaging?)
        # - Time series by person volume
        #     - Time series by person % of bucket
        # - Time series of video calls made, since the chat started

        self.__plot_time_series("TODO", messages)


    def __plot_time_series(self, filename, messages):
        pass
