import glob # used to list files of a specific type recursively
import json # used to parse the messages which are in json format
import emoji # used to facilitate working with emojis

# list message jsons
my_path = '../private-resources/messages'
file_names = glob.glob(my_path + '/**/message*.json', recursive=True)

output_file_name = '../resources/messages.csv'
output_file = open(output_file_name, 'w')
# write csv headers to the output file
output_file.write(",".join(['timestamp','emojis'])+'\n')

# https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
    return obj

# parse a single json
def process_file(file_name):
    file = open(file_name)
    file_content = file.read()
    data = json.loads(file_content, object_hook=parse_obj)

    for message in data['messages']:
        timestamp = str(message['timestamp_ms'])
        content = '' if 'content' not in message else message['content']
        emojis = '' if not content else ''.join(ch for ch in content if ch in emoji.UNICODE_EMOJI)
        output_file.write(",".join([timestamp,emojis])+'\n')
    file.close()
        

for file_name in file_names:
    process_file(file_name)

output_file.close()