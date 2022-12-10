from bs4 import BeautifulSoup
from aiostream import stream
from data import Page, ALL_URLS
from get_pages import get_all_pages_html, get_all_links_from_page, find_parent_link
from tqdm.asyncio import tqdm
from typing import Optional
import warnings


async def wiki_url_parse(urls: list[str | Page], parse_speed: int, count: int = 6, article_to_find: Page | None = None,
                         start=False):
    warnings.simplefilter("ignore", UserWarning)
    if not count:
        print(f"No more tries...can't find end url")
        return False, None
    print(f"\n{'-'.ljust(30, '-')}\nWe have {count} more tries...\n{'-'.ljust(30, '-')}\n")
    find_end_article, last_stage, all_links = await link_collector(urls, article_to_find, parse_speed=parse_speed)
    if find_end_article:
        return True, last_stage
    ALL_URLS.all_pages.update(urls)
    urls = None
    result, stage = await wiki_url_parse(list(all_links), parse_speed=parse_speed, article_to_find=article_to_find,
                                         count=count - 1)
    if result:
        ALL_URLS.path.append(stage)
        if start:
            return True
        return result, await find_parent_link(stage)
    return False, None


async def link_collector(urls: list[str], article_to_find: Page, parse_speed: int) -> \
        tuple[bool, Optional[str], Optional[set[str]]]:
    all_links = set()
    print(f"Check next set of Links...\n\n")
    with tqdm(urls) as pbar:
        async for link_cluster in stream.chunks(generator(pbar), parse_speed):
            pages = await get_all_pages_html(link_cluster)
            for page in pages:
                if page.url in ALL_URLS.all_pages:
                    continue
                bs = BeautifulSoup(page.html, 'lxml')
                links = await get_all_links_from_page(bs)
                if article_to_find.url in links:
                    print(f"\n{'-'.ljust(30, '-')}\nFind END URL in {page.url}\n{'-'.ljust(30, '-')}\n\n")
                    pbar.close()
                    return True, page.url, None
                ALL_URLS.pages_structure[page.url] = list(links)
                all_links.update(links)
    return False, None, all_links

async def check_if_article_exist(page: Page) -> bool:
    bs = BeautifulSoup(page.html, 'lxml')
    validation = bs.find('div', {'id': 'bodyContent'}).find('div', {'class': 'no-article-text-sister-projects'})
    if validation:
        return False
    return True


async def prepare_link_to_validation(link: str):
    urls = [link, ]
    pages = await get_all_pages_html(urls)
    validation = await check_if_article_exist(pages[0])
    return validation, pages[0]


async def generator(data):
    for i in data:
        yield i
