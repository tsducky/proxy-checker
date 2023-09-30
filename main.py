from datetime import datetime
import zoneinfo
import asyncio
import aiohttp
from colorama import Fore

zone = zoneinfo.ZoneInfo("Europe/Moscow")

with open("proxies.txt") as file:
    proxy_list = [row.strip() for row in file]

async def check_proxy(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.ipify.org/?format=json', proxy=f"http://{proxy}", timeout=10) as response:
                print(Fore.GREEN + '[' + datetime.now(zone).strftime('%H:%M:%S') + ']' + f'{proxy} valid')
            
                with open('valid.txt', 'a') as vaild:
                    vaild.write(proxy + '\n')

    except aiohttp.ClientError:
        print(Fore.RED + '[' + datetime.now(zone).strftime('%H:%M:%S') + ']' + f'{proxy} invalid proxy')
    except asyncio.exceptions.TimeoutError:
        print(Fore.RED + '[' + datetime.now(zone).strftime('%H:%M:%S') + ']' + f'{proxy} invalid proxy')
async def main():
    tasks = [asyncio.create_task(check_proxy(proxy)) for proxy in proxy_list]
    print(Fore.WHITE + '[' + datetime.now(zone).strftime('%H:%M:%S') + ']' + f' Starting ...')
    await asyncio.gather(*tasks)

asyncio.run(main())