import requests, xmltodict,icecream as ic
import re, os
import argparse
import aiohttp
import asyncio
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

async def recursive_call(url, home_path):
    if ('.' in url[-7:]):
        await generate_download_data(url, home_path)
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
                await recursive_call(url+href_value, home_path)

async def generate_download_data(url, home_path):
    file_path = get_file_path(url)
    full_file_path = home_path+file_path
    await download_file(url, full_file_path)

def get_file_path(url):
    path_array = url.replace("%20", " ").split('/')[3:-1]
    return os.path.join(*path_array)



# async def download_file(url, destination_path):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             content = await response.read()
#             with open(destination_path, "wb") as f:
#                 f.write(content)


async def download_file(url, destination_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

            # Create a tqdm progress bar
            progress_bar = tqdm_asyncio.tqdm(total=len(content), desc="Downloading file")

            # Write the content to the destination file while updating the progress bar
            with open(destination_path, "wb") as f:
                for chunk in progress_bar.iterable(content):
                    f.write(chunk)

async def main():
    parser = argparse.ArgumentParser()


    parser.add_argument('url')           # positional argument
    parser.add_argument('-d', '--dest')      # option that takes a value
    args = parser.parse_args()


    print(f"Processing file: {args}")

    # url = "http://10.16.100.206/ftps3/"
    await recursive_call(args.url, args.dest)

if __name__ == "__main__":
    asyncio.run(main())