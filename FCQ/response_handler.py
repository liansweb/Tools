import os
import httpx
import asyncio

async def async_request(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url,timeout=2)
        print(resp.status_code)

target_dir_path = "/Applications/All_folder/toolsProject/tools/FCQ/2CVE漏洞POC目标/test/"

file_names = os.listdir(target_dir_path)

for file_name in file_names:
    file_paths = []
    with open(target_dir_path + file_name, "r") as fp:
        file_paths = fp.readlines()
    
    loop = asyncio.get_event_loop()
    try:
        tasks = [asyncio.ensure_future(async_request(url.strip())) for url in file_paths]
        loop.run_until_complete(asyncio.gather(*tasks))
    except httpx.ConnectTimeout as e:
        continue
