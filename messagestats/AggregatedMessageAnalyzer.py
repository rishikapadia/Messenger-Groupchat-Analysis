from datetime import datetime
from collections import Counter
import os


OUTPUT_DIRECTORY = "statistics/"
OUTPUT_FILENAME = "statistics.txt"

# JSON field names
MESSAGE_TYPE = "type"
GENERIC_MESSAGE_TYPE = "Generic"
MESSAGE_CONTENT = "content"
TIMESTAMP_MS = "timestamp_ms"
SENDER_NAME = "sender_name"

NUM_TOP_DATES_TO_PUBLISH = 5


"""
Outputs a txt file with different stats on each line
"""
class AggregatedMessageAnalyzer:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        self.output_file_path = self.output_directory_path + OUTPUT_FILENAME
        return


    def generate_stats(self, messages, participants):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)
        self.file = open(self.output_file_path, "w")

        self.__publish_totals(messages, participants)
        self.__publish_messages_per_day(messages)

        self.file.close()


    def __publish_totals(self, messages, participants):
        self.__write_data(str(len(messages)) + " messages")
        self.__write_data(str(len(participants)) + " participants")


    def __publish_messages_per_day(self, messages):
        message_dates = [datetime.fromtimestamp(m[TIMESTAMP_MS]/1000).date() for m in messages]

        num_total_messages = len(messages)
        num_dates_with_messages = len(set(message_dates))

        earliest_date = min(message_dates)
        latest_date = max(message_dates)
        num_total_days = (latest_date - earliest_date).days

        self.__write_data("Total number of days: " + str(num_total_days))
        self.__write_data("Days with messages: " + str(num_dates_with_messages))

        def round(decimal):
            return str(int(decimal * 100) / 100)
        self.__write_data("Average number of messages per day: " + round(num_total_messages/num_total_days))
        self.__write_data("Avg number of messages per day where there are at least 1 message that day: " \
            + round(num_total_messages/num_dates_with_messages))
        self.__write_data("% of days that had no messages, since our first message: " \
            + round((1 - num_dates_with_messages/num_total_days)*100) + "%")

        # Get the days with the highest number of messages
        counts = Counter(message_dates)
        most_active_dates = counts.most_common(NUM_TOP_DATES_TO_PUBLISH)
        self.__write_data("\nDates with the most messages:")
        for i in range(len(most_active_dates)):
            self.__write_data(str(i + 1) + ". " + most_active_dates[i][0].strftime("%B %d, %Y") \
                + ": " + str(most_active_dates[i][1]) + " messages")
        self.__write_data("\n")

        # TODO get a sample message from the top day, and search for it in the chat history
        # top_active_date = most_active_dates[0][0]
        from IPython import embed; embed() # TODO remove after done debugging


    def __publish_TODO(self, messages):
        pass


    def __write_data(self, text):
        self.file.write(text + "\n")
