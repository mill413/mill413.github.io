import logging
import tomllib
from datetime import datetime, timedelta, timezone
from typing import Generator, Self

import requests
from arxiv import Result
from mdBuilder import MdBuilder
from mdElement import *

logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s",
                    datefmt="%Y/%m/%d %H:%M:%S",
                    level=logging.INFO)

# load config from file
with open("daily-arxiv/config.toml", "rb") as f:
    config = tomllib.load(f)


class Paper:
    def __init__(self,
                 date: datetime,
                 title: str,
                 authors: list[Result.Author],
                 id: str,
                 url: str) -> None:
        self.date: datetime = date
        self.title: str = title
        self.authors: str = f"{authors[0].name} et al." if len(
            authors) > 1 else authors[0].name
        self.id: str = id
        self.url: str = url
        self.code: str | None = None

    def get_code_link(self):
        query_url = f"https://arxiv.paperswithcode.com/api/v0/papers/{self.id}"
        try:
            result = requests.get(query_url).json()
            if "official" in result and result["official"]:
                self.code = result["official"]["url"]
            else:
                self.code = None
        except:
            self.code = None

    def __repr__(self) -> str:
        return str({
            "date": self.date.strftime("%Y/%m/%d"),
            "title": self.title,
            "authors": self.authors,
            "id": self.id,
            "url": self.url,
            "code": self.code
        })

    def __lt__(self, other: Self) -> bool:
        return self.date < other.date

    def __gt__(self, other: Self) -> bool:
        return self.date > other.date

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id


def log(message: str):
    logging.info(message)


def concat_filters(filters: list[str]) -> str:
    return "OR".join([
        f"\"{filter}\"" if " " in filter
        else filter
        for filter in filters
    ])


def parse_papers(results: Generator[Result, None, None]) -> list[Paper]:
    return [Paper(
        date=result.published.date(),
        title=result.title,
        authors=result.authors,
        id=result.get_short_id(),
        url=result.entry_id
    ) for result in results]


def content_to_md(content: dict, file: str):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    topic_block = []
    for topic, papers in content.items():
        topic_block.append(Heading(2, topic))
        topic_block.append(Table(
            header=["论文", "代码链接"],
            content=[
                [Link(url=paper.url, text_or_image=paper.title),
                 Link(url=paper.code, text_or_image=Bold(
                     "link")) if paper.code else ""
                 ] for paper in papers
            ]
        ))

    MdBuilder(
        FrontMatter({
            "layout": "post",
            "icon": "fas fa-archive",
            "order": "4",
            "toc": "true",
        }),
        f"> 更新于 {now}\n"+"{: .prompt-info}",
        topic_block
    ).write_to_file(file)
