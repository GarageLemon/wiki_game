import asyncio
from bs4 import BeautifulSoup
from get_pages import get_all_pages_html
from wiki_parser import wiki_url_parse, prepare_link_to_validation
from data import ALL_URLS, Page
from anytree import Node, RenderTree


async def prepare_url(url_string):
    # TODO add regular exp to check that url contains full wiki url
    if 'https://en.wikipedia.org/wiki/' not in url_string:
        url_string = f"https://en.wikipedia.org/wiki/{url_string.strip().replace(' ', '_')}"
    return url_string.strip()


async def get_title(html: str) -> str:
    bs = BeautifulSoup(html, 'lxml')
    return bs.h1.text


async def check_url(input_text: str) -> Page:
    while True:
        validation, url = await prepare_link_to_validation(await prepare_url(str(input(f"{input_text} "))))
        if validation:
            return url
        print(f"This article doesn't exist, or you've typed something wrong. Try again...")


async def make_finale_pages_list(urls: list, start_url: Page, end_url: Page) -> list[Page]:
    pages = await get_all_pages_html(urls)
    pages.append(start_url)
    pages.insert(0, end_url)
    pages.reverse()
    return pages


async def make_article_tree(titles: list[str], nodes_list=list()) -> list[Node]:
    for ind, x in enumerate(titles):
        if not ind:
            n = Node(str(x))
        else:
            n = Node(str(x), parent=nodes_list[ind - 1])
        nodes_list.append(n)
    return nodes_list


async def prepare_urls_and_start():
    start_url = await check_url('Choose a start url/title:')
    end_url = await check_url('Choose an end url/title:')
    result = await wiki_url_parse([start_url, ], article_to_find=end_url, start=True)
    if result:
        pages = await make_finale_pages_list(ALL_URLS.path, start_url, end_url)
        titles = [await get_title(path.html) for path in pages]
        tree = await make_article_tree(titles)
        print(f"Search Result:\n\n{RenderTree(tree[0]).by_attr()}\n")
    else:
        print(f"Can't find URL, try again..")


if __name__ == '__main__':
    asyncio.run(prepare_urls_and_start())