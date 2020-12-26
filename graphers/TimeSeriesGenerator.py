from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import os


OUTPUT_DIRECTORY = "graphs/"
OUTPUT_FILE_FORMAT = ".png"

# JSON field names
TIMESTAMP_MS = "timestamp_ms"
SENDER_NAME = "sender_name"


class TimeSeriesGenerator:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        return


    def generate_graphs(self, messages):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

        self.__plot_message_volume(messages)
        self.__plot_person_percentage_volume(messages)


    def __plot_message_volume(self, messages):
        def time_bucket(time):
            # Hash together all messages in the same month
            message_date = datetime.fromtimestamp(time/1000).date()
            return date(year=message_date.year, month=message_date.month, day=1)
        times = [time_bucket(m[TIMESTAMP_MS]) for m in messages]
        counts = Counter(times).most_common()
        
        first_bucket, last_bucket = min(times), max(times)
        def delta_months(month):
            return (month.year - first_bucket.year) * 12 + (month.month - first_bucket.month)
        num_month_buckets = delta_months(last_bucket) + 1
        x_labels = [(first_bucket + relativedelta(months=i)).strftime("%B %Y") for i in range(num_month_buckets)]

        x_indices = range(num_month_buckets)

        values = [0] * num_month_buckets
        for month, count in counts:
            index = delta_months(month)
            values[index] = count

        figure, axes = plt.subplots()
        figure.set_size_inches(9, 4)
        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        
        axes.set_title("# of Messages Per Month")
        axes.set_ylabel("Messages Per Month")
        axes.set_xticks(x_indices)
        axes.set_xticklabels(x_labels, rotation=90)

        axes.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        axes.plot(x_indices, values)

        figure.tight_layout()
        plt.savefig(self.output_directory_path + "messages_time_series" + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")

        # Add circles/annotations for the min and max months
        most_count, least_count = counts[0], counts[-1]

        def add_marker(date, value, color):
            x_index = delta_months(date)
            oval = Ellipse((x_index, value), 1, 400, color=color, fill=False)
            axes.add_artist(oval)
            axes.annotate('{:,}'.format(value), \
                xy=(x_index, value), \
                xytext=(0, 6), \
                textcoords="offset points", \
                color=color, \
                ha="center", va="bottom")

        add_marker(most_count[0], most_count[1], 'g')
        add_marker(least_count[0], least_count[1], 'r')

        plt.savefig(self.output_directory_path + "messages_time_series_min_max" + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")


    def __plot_person_percentage_volume(self, messages):
        def time_bucket(time):
            # Hash together all messages in the same month
            message_date = datetime.fromtimestamp(time/1000).date()
            return date(year=message_date.year, month=message_date.month, day=1)
        times = [time_bucket(m[TIMESTAMP_MS]) for m in messages]
        total_counts = Counter(times).most_common()
        
        first_bucket, last_bucket = min(times), max(times)
        def delta_months(month):
            return (month.year - first_bucket.year) * 12 + (month.month - first_bucket.month)
        num_month_buckets = delta_months(last_bucket) + 1
        x_indices = range(num_month_buckets)
        x_labels = [(first_bucket + relativedelta(months=i)).strftime("%B %Y") for i in range(num_month_buckets)]

        # Calculate the total count and per person, so we can get a ratio per person
        times_and_sender = [(time_bucket(m[TIMESTAMP_MS]), m[SENDER_NAME]) for m in messages]

        total_counts_per_month = np.zeros(num_month_buckets)
        counts_per_person_per_month = {}
        for month, person in times_and_sender:
            if person not in counts_per_person_per_month:
                counts_per_person_per_month[person] = np.zeros(num_month_buckets)
            index = delta_months(month)
            total_counts_per_month[index] += 1
            counts_per_person_per_month[person][index] += 1

        for person in counts_per_person_per_month:
            counts_per_person_per_month[person] = counts_per_person_per_month[person] / total_counts_per_month

        # Plot as filled-in area
        figure, axes = plt.subplots()
        figure.set_size_inches(9.5, 4)
        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        
        axes.set_title("% of Messages Per Month")
        axes.set_ylabel("% of Messages Per Month")
        axes.set_xticks(x_indices)
        axes.set_xticklabels(x_labels, rotation=90)

        axes.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0%}".format(x)))

        y_values = []
        legend_labels = []
        y_values.append(np.zeros(num_month_buckets))
        for person in counts_per_person_per_month:
            y_values.append(counts_per_person_per_month[person])
            name = person.split()
            legend_labels.append(" ".join([name[0], name[1][:1]]))

        cumulative_sum = np.zeros(num_month_buckets)
        for i in range(len(y_values) - 1):
            cumulative_sum = cumulative_sum + y_values[i]
            axes.fill_between(x_indices, cumulative_sum, cumulative_sum + y_values[i+1], label=legend_labels[i])

        axes.legend(bbox_to_anchor=(1.15, 1.05))

        figure.tight_layout()
        plt.savefig(self.output_directory_path + "person_percentage_time_series" + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")
