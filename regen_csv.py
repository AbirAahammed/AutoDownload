import requests, xmltodict,icecream as ic
import re, os
import argparse
import aiohttp
import asyncio
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

def recursive_call(url, writer):
    if ('.' in url[-7:]):
        generate_download_data(url, writer)
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
                 recursive_call(url+href_value, writer)

def generate_download_data(url, writer):
    file_path = get_file_path(url)
    print("{},{}".format(url,file_path))
    # writer.writerow("{},{}".format(url,file_path))

def get_file_path(url):
    path_array = url.replace("%20", " ").split('/')[3:-1]
    return os.path.join(*path_array)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')           # positional argument
    args = parser.parse_args()
    import csv

    # open the file in the write mode
    f = open('test.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow("URL,Path")

    # close the file
    recursive_call(args.url, writer)
    f.close()


if __name__ == "__main__":
    main()