from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import unicodedata as ud
import os


OUTPUT_DIRECTORY = "graphs/"
OUTPUT_FILE_FORMAT = ".png"

# JSON field names
SENDER_NAME = "sender_name"
MESSAGE_CONTENT = "content"
REACTIONS = "reactions"
REACTION = "reaction"
ACTOR = "actor"

TOP_REACTIONS_PER_PERSON = 5
BAR_GROUP_MARGIN = 0.2


class BarGraphsGenerator:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        return


    def generate_graphs(self, messages):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

        self.__plot_messages_per_person(messages)
        self.__plot_reactions_per_person(messages)
        self.__plot_top_reactions_per_person(messages)


    def __plot_messages_per_person(self, messages):
        count_by_person = Counter([message[SENDER_NAME] for message in messages]).most_common()
        self.__volume_bar_plot_helper("messages_per_person", count_by_person, len(messages), \
            "Number of messages per person", "Number of Messages")


    def __plot_reactions_per_person(self, messages):
        reactions_per_person = self.__get_reactions_per_person(messages)
        count_by_person = {}
        for person in reactions_per_person:
            count_by_person[person] = len(reactions_per_person[person])
        count_by_person = Counter(count_by_person).most_common()
        self.__volume_bar_plot_helper("reactions_per_person", count_by_person, len(messages), \
            "Number of reactions per person", "Number of Reactions")


    def __get_reactions_per_person(self, messages):
        reactions_by_person = {}
        for message in messages:
            if REACTIONS not in message:
                continue
            for reaction in message[REACTIONS]:
                if ACTOR not in reaction or REACTION not in reaction:
                    print("Unexpected error: Reaction JSON has no \"actor\" or \"reaction\" field!")
                    continue
                if reaction[ACTOR] not in reactions_by_person:
                    reactions_by_person[reaction[ACTOR]] = []
                reactions_by_person[reaction[ACTOR]].append(reaction[REACTION])
        return reactions_by_person


    def __volume_bar_plot_helper(self, filename, count_by_person, total_count, title, y_label):
        x_labels = list([name for name, count in count_by_person])
        y_values = list([count for name, count in count_by_person])
        x_indices = np.arange(len(x_labels))

        figure, axes = plt.subplots()
        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        
        axes.set_title(title)
        axes.set_ylabel(y_label)
        axes.set_xticks(x_indices)
        axes.set_xticklabels(x_labels, rotation=75)

        axes.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        
        rects = axes.bar(x_indices, y_values)
        axes.bar(x_labels, y_values)
        for rect in rects:
            height = rect.get_height()
            axes.annotate('{:,}'.format(height), \
                xy=(rect.get_x() + rect.get_width() / 2, height), \
                # vertical offset
                xytext=(0, 3), \
                textcoords="offset points", \
                ha="center", va="bottom")
            axes.annotate('{:.0%}'.format(height/total_count), \
                xy=(rect.get_x() + rect.get_width() / 2, height), \
                xytext=(0, 15), \
                textcoords="offset points", \
                color='b', \
                ha="center", va="bottom")

        figure.tight_layout()
        plt.savefig(self.output_directory_path + filename + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")


    def __plot_top_reactions_per_person(self, messages):
        reactions_per_person = self.__get_reactions_per_person(messages)
        
        top_reactions_per_person = {}
        for person in reactions_per_person:
            top_reactions_per_person[person] = Counter(reactions_per_person[person]).most_common()

        x_labels = list(top_reactions_per_person.keys())
        x_labels.sort()

        y_values, bar_reactions_per_person = [], []
        for person in x_labels:
            reactions_counts = top_reactions_per_person[person]
            bar_reactions_per_person.append([reaction.encode('latin1').decode('utf8') for reaction, count in reactions_counts])

            # normalize counts by person
            total_reactions_per_person = np.array([count for reaction, count in reactions_counts])
            y_values.append(total_reactions_per_person / sum(total_reactions_per_person))

        bar_width = (1 - BAR_GROUP_MARGIN) / TOP_REACTIONS_PER_PERSON  # the width of each bar
        x_locations = [(np.arange(len(x_labels)) + x * bar_width) for x in range(TOP_REACTIONS_PER_PERSON)]  # the bar locations

        fig, ax = plt.subplots()
        fig.set_size_inches(8, 4.5)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        ax.set_title("Top Reactions per Person")
        ax.set_ylabel("% of Reactions (per Person)")
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0%}".format(x)))
        ax.set_xticks(x_locations[0] + (1 - BAR_GROUP_MARGIN - bar_width) / 2)
        ax.set_xticklabels(x_labels, rotation=75)

        def replace_unsupported_emojis(emoji):
            if emoji == '👍':
                return 'U'
            if emoji == '👎':
                return 'D'
            return emoji

        for index in range(TOP_REACTIONS_PER_PERSON):
            rects = ax.bar(x_locations[index], [reactions[index] for reactions in y_values], bar_width)
            labels_per_bar = [replace_unsupported_emojis(person[index]) for person in bar_reactions_per_person]
            for i, rect in enumerate(rects.get_children()):
                height = rect.get_height()
                ax.annotate(labels_per_bar[i], \
                    xy=(rect.get_x() + rect.get_width() / 2, height), \
                    xytext=(0, 3), \
                    textcoords="offset points", \
                    ha="center", va="bottom")

        fig.tight_layout()
        plt.savefig(self.output_directory_path + "top_reactions_per_person" + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")
