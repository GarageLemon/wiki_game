from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AllUrls:
    pages_structure: dict = field(default_factory=dict)
    all_pages: set = field(default_factory=set)
    path: list = field(default_factory=list)


@dataclass(eq=True, slots=True, kw_only=True, unsafe_hash=True)
class Page:
    url: str
    html: str


ALL_URLS = AllUrls()
