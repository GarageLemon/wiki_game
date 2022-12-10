import httpx
from httpx import AsyncClient
import asyncio
import re
from bs4 import BeautifulSoup
from data import Page, ALL_URLS


async def get_page_html(client: AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text


async def get_all_pages_html(urls: list[str | Page]) -> list[Page]:
    async with httpx.AsyncClient(timeout=30) as client:
        if type(urls[0]) == Page:
            return urls
        pages = []
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(get_page_html(client, url)))
        all_info = await asyncio.gather(*tasks)
        for info, url in zip(all_info, urls):
            pages.append(Page(url=url, html=info))
        return pages


async def get_all_links_from_page(bs: BeautifulSoup) -> set[str]:
    links = set(f"https://en.wikipedia.org{link.attrs['href']}" for link in bs.find('div', {'id': 'bodyContent'})
                .find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')) if 'href' in link.attrs)
    return links


async def find_parent_link(stage: str) -> str:
    for key, value in ALL_URLS.pages_structure.items():
        if stage in value:
            return key