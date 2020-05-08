import re # regex library to extract specific portions from the source txt file

# converts a single hex code to a utf8 encoded string
# eg.: '1F1FF' ---> '\xf0\x9f\x87\xbf'
def single_hex_to_utf8(single_hex_string):
    utf8_encoding = chr(int(single_hex_string, 16)).encode('utf-8')
    utf8_string = str(utf8_encoding)
    return re.search(r"'(.*)'", utf8_string).group(1)
    
# converts a string consisting of multiple hex codes to a utf8 encoded string
# eg.: '1F1FF 1F1FC' ---> '\xf0\x9f\x87\xbf\xf0\x9f\x87\xbc'
def full_hex_to_utf8(hex_string):
    utf8_list = map(lambda hex : single_hex_to_utf8(hex), hex_string.split())
    return "".join(utf8_list)

# converts a string consisting of multiple hex codes to a single utf8 encoded bytelist
# eg.: '1F1FF 1F1FC' ---> b'\xf0\x9f\x87\xbf\xf0\x9f\x87\xbc'
def hex_to_utf8_bytes(hex_string):
    result = bytes()
    for hex in hex_string.split():
        b = chr(int(hex, 16)).encode('utf-8')
        for i in range(0, len(b)):
            result += b[i:i+1]
    return result

# Open and read the input file
input_file_name = 'resources/emoji-test.txt'
input_file = open(input_file_name, 'r')
input_file_text = input_file.read()

# Create the output file
output_file_name = 'resources/emoji-data-table.csv'
output_file = open(output_file_name, 'w')
# write csv headers to the output file
output_file.write(",".join(['emoji','hex_string','utf8_string','emoji_desc'])+'\n')

# parse the input txt file
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

    # decode hex into the actual emoji
    emoji = hex_to_utf8_bytes(hex_string).decode('utf-8')
    
    # write data to the output file
    output_file.write(",".join([emoji,hex_string,utf8_string,emoji_desc])+'\n')

input_file.close()
output_file.close()