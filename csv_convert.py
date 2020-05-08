import glob # used to list files of a specific type recursively
import json # used to parse the messages which are in json format
import csv
import re

my_path = 'private-resources/messages'
file_names = glob.glob(my_path + '/**/*.json', recursive=True)

output_file_name = 'resources/messages.csv'
output_file = open(output_file_name, 'w')
# write csv headers to the output file

emoji_codes = []
with open('resources/emoji-data-table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first = True
    for row in csv_reader:
        # skip header
        if first:
            first = False
            continue
        emoji_codes.append(row[1])

def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
        elif isinstance(obj[key], list):
            obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
        pass
    return obj

def process_file(file_name):
    file = open(file_name)
    file_content = file.read()
    data = json.loads(file_content, object_hook=parse_obj)
    print(data)

'''
    for message in data['messages']:
        timestamp = message['timestamp_ms']
        content = '' if 'content' not in message else message['content']
        content = bytes(content, 'utf-8')
        #print(timestamp, content)
'''

process_file(file_names[10])