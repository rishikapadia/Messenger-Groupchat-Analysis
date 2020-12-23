import glob, json


INPUT_FILENAMES_REGEX = "*.json"

# JSON field names
PARTICIPANTS = "participants"
MESSAGES = "messages"
PARTICIPANT_NAME = "name"


class JsonMessageParser:
    def __init__(self, input_directory_path):
        self.input_directory_path = input_directory_path
        return

    def parse_message_data(self):
    	all_messages = []
    	all_participants = []
    	filenames = glob.glob(self.input_directory_path + INPUT_FILENAMES_REGEX)
    	for filename in filenames:
    		with open(filename) as json_data:
    			data = json.load(json_data)
    			all_messages += data[MESSAGES]
    			all_participants += data[PARTICIPANTS]
    	return all_messages, self.__get_participant_names(all_participants)

    def __get_participant_names(self, all_participants):
    	participant_names = set()
    	for p in all_participants:
    		participant_names.add(p[PARTICIPANT_NAME])
    	return participant_names
