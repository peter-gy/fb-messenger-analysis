import re # regex library to extract specific portions from the source txt file

# converts a single hex code to a 4-char utf8 encoded string
# eg.: '1F1FF' ---> '\u00f0\u009f\u0087\u00bf'
def single_hex_to_utf8(single_hex_string):
    utf8_encoding = chr(int(single_hex_string, 16)).encode('utf-8')
    utf8_string = str(utf8_encoding)
    content = re.search(r"'(.*)'", utf8_string).group(1)
    return re.sub(r'\\x', r'\\u00', content)
    
# converts a string consisting of multiple hex codes to a 4-char utf8 encoded string
# eg.: '1F1FF 1F1FC' ---> '\u00f0\u009f\u0087\u00bf\u00f0\u009f\u0087\u00bc   '
def full_hex_to_utf8(hex_string):
    utf8_list = map(lambda hex : single_hex_to_utf8(hex), hex_string.split())
    return "".join(utf8_list)

# Open and read the input file
input_file_name = 'resources/emoji-test.txt'
input_file = open(input_file_name, 'r')
input_file_text = input_file.read()

# Create the output file
output_file_name = 'resources/emoji-data-table.csv'
output_file = open(output_file_name, 'w')

for line in input_file_text.splitlines():
    # skip line if it is empty or it is commented out
    if not line or line[0] == '#': continue
    # extract unicode hex from line before the semicolon ;
    semicolon_idx = line.index(";")
    hex_groups = re.findall(r'([0-9A-F]+ )', line[:semicolon_idx])
    # join the groups and remove last white space
    hex_string = "".join(hex_groups)[:-1]

    # extract emoji description
    emoji_desc = re.search(r'E[0-9]+\.[0-9]+ (.*)', line).group(1)

    # convert the hexadecimal string to utf8 encoded string
    utf8_string = full_hex_to_utf8(hex_string)
    
    # write data to the output file
    output_line = ",".join([hex_string,utf8_string,emoji_desc])
    output_file.write(output_line+'\n')

input_file.close()
output_file.close()