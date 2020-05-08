import glob

my_path = 'private-resources/messages'
files = glob.glob(my_path + '/**/*.json', recursive=True)
