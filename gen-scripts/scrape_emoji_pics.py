from bs4 import BeautifulSoup
import requests
import re

# specify headers for the http request
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

# set up the bs4 object with the using the response of the http request
url = "https://emojipedia.org/apple/ios-13.3/"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

# query for the emoji-grid ul
emoji_grid = soup.find('ul', class_='emoji-grid')

# Create the output file
output_file_name = '../resources/emoji-img-links.txt'
output_file = open(output_file_name, 'w')

# query for images with 'data-src' attribute containing anything
img_tags = emoji_grid.find_all('img')

# workaround needed since images are lazily loaded
# if an image is loaded, the sought url can be read from the 'src' attribute of the img tag
# else the 'src' attribute of the tag is set to /static/img/lazy.svg 
# and the url is stored in the 'data-src' attribute
def extract_img_url(img_tag):
    img_src = img_tag.get('src')
    img_data_src = img_tag.get('data-src')
    return img_data_src if 'static' in img_src else img_src

# write the png source urls to the output file
img_urls = [*map(extract_img_url, img_tags)]
output_file.write("\n".join(img_urls))

output_file.close()