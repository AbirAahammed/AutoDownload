import requests, xmltodict,icecream as ic
import re

def recursive_call(url):
    if ('.' in url[-7:]):
        generate_download_data(url)
        return
    
    x = requests.get(url)
    if ('404 Not Found' in x.text):
        return
    table = x.text.split("<table>",1)[1].split("</table>", 1)[0]
    
    table_list = [x.strip() for x in table.split("\n")[4:]]
    for i in table_list:
    # Define a regular expression to match table data
        table_data_regex = r'<td.*?>(.*?)</td>'

        # Extract the table data from the HTML string
        table_data = re.findall(table_data_regex, i)

        # Print the table data
        if len(table_data) != 0:
            href_regex = r'(?<=href=")([^"]+)(?=">)'
            match = re.search(href_regex, table_data[1])
            href_value = match.group(1)
            if href_value != "Games/" or href_value != "Software/":
                recursive_call(url+href_value)

def generate_download_data(value):
    print(value)

url = "http://10.16.100.206/ftps3/"
recursive_call(url)
