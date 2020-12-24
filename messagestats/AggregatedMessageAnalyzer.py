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
REACTIONS = "reactions"
REACTION = "reaction"
ACTOR = "actor"
VIDEOS = "videos"
PHOTOS = "photos"
GIFS = "gifs"

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
        self.__publish_top_reacted_messages(messages, participants)

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

        # Get a sample message from the top day, so we can search for the date in the chat history afterward
        top_active_date = most_active_dates[0][0]
        message_from_top_active_date = messages[message_dates.index(top_active_date)]
        self.__write_data("\nSample message from the most active date: \"" \
            + message_from_top_active_date[MESSAGE_CONTENT] + "\"\n\n")


    def __publish_top_reacted_messages(self, messages, participants):
        num_participants = len(participants)
        top_reacted_messages = {}
        for message in messages:
            if REACTIONS not in message:
                continue
            num_reactions = len(message[REACTIONS])
            # Assumming people don't react to their own messages, the most reactions
            # you can expect is `len(participants) - 1`. This gets all messages that
            # have that maximum, or almost had the maximum.
            if num_reactions < num_participants - 2:
                continue
            if num_reactions not in top_reacted_messages:
                top_reacted_messages[num_reactions] = []
            top_reacted_messages[num_reactions].append(message)

        for i in range(num_participants - 2, num_participants + 1)[::-1]:
            if i in top_reacted_messages:
                self.__write_data(str(len(top_reacted_messages[i])) \
                    + " messages with " + str(i) + " reactions")

        if (num_participants - 1) not in top_reacted_messages:
            return
        
        # Out of the ones with (num_participants - 1) reactions, how many had the sender give a reaction?
        self_reacted = [m for m in top_reacted_messages[num_participants - 1] if m[SENDER_NAME] in [r[ACTOR] for r in m[REACTIONS]]]
        self.__write_data("\n" + str(len(self_reacted)) + " messages with " + str(num_participants - 1) \
            + " reactions where the sender also reacted.")

        # Out of the ones with (num_participants - 1) reactions, how many were all the same reaction?
        same_max_reactions = [m for m in top_reacted_messages[num_participants - 1] if len(set([r[REACTION] for r in m[REACTIONS]])) == 1]
        self.__write_data("Out of the messages with " + str(num_participants - 1) \
            + " reactions, " + str(len(same_max_reactions)) + " had the same reaction.")
        self.__write_data("Of those, \n" \
            + str(len([a for a in same_max_reactions if MESSAGE_CONTENT in a])) + " were text, \n" \
            + str(len([a for a in same_max_reactions if VIDEOS in a])) + " were videos, \n" \
            + str(len([a for a in same_max_reactions if PHOTOS in a])) + " were photos, and \n" \
            + str(len([a for a in same_max_reactions if GIFS in a])) + " were gifs.\n") \

        self.__write_data("\nHere are those messages, or the message right before so we can search for it:")
        for i, message in enumerate(same_max_reactions):
            if MESSAGE_CONTENT in message:
                self.__write_data(str(i+1) + ". Text: \"" + message[MESSAGE_CONTENT] + "\"")
            else:
                # find a message that is near that one, such that it contains text that we can search for
                index_in_list = messages.index(message)
                if index_in_list < 0:
                    self.__write_data(str(i+1) + ". ERROR could not find message?!")
                    continue
                while index_in_list >= 0 and (MESSAGE_CONTENT not in messages[index_in_list] or len(messages[index_in_list][MESSAGE_CONTENT]) < 10):
                    index_in_list -= 1
                if (index_in_list < 0):
                    self.__write_data(str(i+1) + ". ERROR no text messages sent prior to this message")
                    continue
                self.__write_data(str(i+1) + ". \"" + messages[index_in_list][MESSAGE_CONTENT] + "\"")


    def __write_data(self, text):
        self.file.write(text + "\n")
