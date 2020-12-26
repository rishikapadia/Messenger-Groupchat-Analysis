This project is to provide interesting statistics about a group chat in Facebook Messenger. This does not use any internal Facebook tools or APIs, and can be used by anyone who downloads their chat history in Facebook's data settings.

### Getting started

1. Download this repository
2. Go to your Facebook settings and download your chat history

    i.) On facebook.com, click the down arrow button in the top right corner, then "Settings & Privacy" and "Settings".

    ii.) "Your Facebook Information".

    iii.) "Download Your Information"

    iv.) Date range: "All of my data", Format: "JSON", Media Quality: "Low"

    v.) "Deselect All", then only select "Messages".

    vi.) Click on "Create File".

    vii.) After you get a notification that the download is complete, download and extract the JSON files for that group chats that you want to analyze. Delete the other files (media, etc.).

    viii.) Put all the JSON messages you want to analyze as an aggregate into a new directory called `input/` in the project root level (inside the folder that contains `main.py`). If you are combining messages from multiple chats, make sure to rename those files so they don't override each other. The names of the JSON files in `input/` don't matter, we will combine them based on the timestamp and other message properties.

3. In the terminal, run `$ <file_path>/main.py`. If you don't want to make that file executable (using chmod), run `$ python3 main.py`
4. Check out the `output/` directory for word clouds, graphs, and other statistics.


### Post-processing

Most of the images and statistics in `output/` can be used directly in a presentation, for example. Here are some caveats for things that can be improved upon:

1. `output/graphs/top_reactions_per_person.png` contains rudimentary emoji labels for the bar plots. `matplotlib` doesn't have robust emoji support on Mac OS by default. As a temporary workaround, I included `output/graphs/top_reactions_per_person.txt` that contains the actual emoji labels, which you can copy and paste into the graph PNG yourself if you'd like higher-quality labels.

2. In `output/statistics/statistics.txt`, I listed out the messages with most reactions of the same reaction. If the message was contained media instead of text, I return the text of a message near it. This is a specific use case for my group chat, where I wanted to be able to search for the text in the chat and copy the screenshot onto a slide presentation.

3. Similar to #2, I included a sample message in `output/statistics/statistics.txt` for the day with the most messages so that I can search and revisit it. The idea was to screenshot messages from that day manually, to summarize why we made so many messages that day. Again, #2 and #3 may not be relevant for most other group chats.

4. For the sake of time, this tool was built for my one group thread's use case. I built it with generic group threads and privacy concerns in mind, but it has not been tested on other group threads, and some logic may not take edge conditions into account. If you have any issues analyzing your chat thread, please reach out to me or submit a PR.
