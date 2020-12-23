from wordcloud import WordCloud
from datetime import datetime
import os, string, re


OUTPUT_DIRECTORY = "wordcloud/"
OUTPUT_FILE_FORMAT = ".png"

# JSON field names
MESSAGE_TYPE = "type"
GENERIC_MESSAGE_TYPE = "Generic"
MESSAGE_CONTENT = "content"
TIMESTAMP_MS = "timestamp_ms"
SENDER_NAME = "sender_name"

EXCLUDE_CALL_JOINED = "joined the video chat."
WORDS_TO_REMOVE = [
    "\u00f0\u009f\u0091\u0080", # eyes emoji
    "\u00e2\u0080\u009c", # quotes
    "\u00e2\u0080\u009d", # quotes
    "â", "Â", "ð", "¤", "ï", "½", "§", "¢", "¥", "ª", "¦", '"',
]
EMOJI_PATTERN = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)


"""
Class that takes in a list of messages and outputs WordCloud images.

Word clouds generated:
- over all messages
- per year
- per person
"""
class WordCloudGenerator:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        return


    def generate_wordclouds(self, messages):
        messages = self.__preprocess_messages(messages)

        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

        # All messages
        self.__save_wordcloud_data("all_messages", messages)

        # Messages per year
        self.__generate_wordclouds_per_year(messages)

        # Messages per person
        self.__generate_wordclouds_per_person(messages)


    def __preprocess_messages(self, messages):
        new_messages = []
        for message in messages:
            if message[MESSAGE_TYPE] != GENERIC_MESSAGE_TYPE:
                continue
            if MESSAGE_CONTENT not in message:
                continue
            if EXCLUDE_CALL_JOINED in message[MESSAGE_CONTENT]:
                continue

            # Note: WordCloud ignores words with contractions
            message[MESSAGE_CONTENT] = message[MESSAGE_CONTENT].replace("\u00e2\u0080\u0099", "'")

            # Remove emojis and other unprintable characters
            message[MESSAGE_CONTENT] = re.sub(EMOJI_PATTERN, '', message[MESSAGE_CONTENT])
            message[MESSAGE_CONTENT] = ''.join([c for c in message[MESSAGE_CONTENT] if c not in WORDS_TO_REMOVE])

            new_messages.append(message)
        return new_messages


    def __generate_wordclouds_per_year(self, messages):
        messages_by_year = {}
        for message in messages:
            year = datetime.fromtimestamp(message[TIMESTAMP_MS]/1000.0).year
            if year not in messages_by_year:
                messages_by_year[year] = [message]
            else:
                messages_by_year[year].append(message)

        for year in messages_by_year:
            self.__save_wordcloud_data("year_" + str(year), messages_by_year[year])


    def __generate_wordclouds_per_person(self, messages):
        messages_by_person = {}
        for message in messages:
            sender_name = message[SENDER_NAME]
            if sender_name not in messages_by_person:
                messages_by_person[sender_name] = [message]
            else:
                messages_by_person[sender_name].append(message)

        for person in messages_by_person:
            self.__save_wordcloud_data(person, messages_by_person[person])


    def __save_wordcloud_data(self, filename, messages):
        all_words = " ".join(m[MESSAGE_CONTENT] for m in messages)
        
        wordcloud = WordCloud(width=800, height=400, max_words=500, background_color="white").generate(all_words)
        wordcloud.to_file(self.output_directory_path + filename + OUTPUT_FILE_FORMAT)
