from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from collections import Counter
import os


OUTPUT_DIRECTORY = "graphs/"
OUTPUT_FILE_FORMAT = ".png"

# JSON field names
MESSAGE_CONTENT = "content"
TIMESTAMP_MS = "timestamp_ms"
SENDER_NAME = "sender_name"


class TimeSeriesGenerator:
    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path + OUTPUT_DIRECTORY
        return


    def generate_graphs(self, messages):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)

        # Time series:
        # - Time series of messages (bucket size = 1 month? window-size averaging?)
        # - Time series by person % of bucket

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
        axes.set_xticklabels(x_labels, rotation=75)

        axes.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        axes.plot(x_indices, values)

        figure.tight_layout()
        plt.savefig(self.output_directory_path + "messages_time_series" + OUTPUT_FILE_FORMAT, \
            format="png", bbox_inches="tight")


    def __plot_person_percentage_volume(self, messages):
        #from IPython import embed; embed();
        sys.exit(0) # TODO remove after done debugging
        pass
