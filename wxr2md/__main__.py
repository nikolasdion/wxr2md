#!/usr/bin/env python3

from pathlib import Path
from xml.etree import ElementTree
from dataclasses import dataclass
import sys

NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

DEFAULT_OUTPUT_FOLDER: Path = Path("./out")


@dataclass
class Post:
    # title displayed in the content, can be None
    title: str
    # name in the URL, useful for filename or unique identifier
    name: str
    # unique ID of the post
    id: str
    content: str
    post_date: str
    post_modified: str
    categories: list[str]

    def from_element(element: ElementTree.Element):
        title = element.find("title").text
        name = element.find("wp:post_name", NAMESPACES).text
        id = element.find("wp:post_id", NAMESPACES).text
        content = element.find("content:encoded", NAMESPACES).text
        post_date = element.find("wp:post_date_gmt", NAMESPACES).text
        post_modified = element.find("wp:post_modified_gmt", NAMESPACES).text
        categories = [e.text for e in element.findall("category")]

        return Post(
            title=title,
            name=name,
            id=id,
            content=content,
            post_date=post_date,
            post_modified=post_modified,
            categories=categories,
        )

    def to_md(self) -> str:
        md = ""
        md += f"# {self.title}\n\n"

        for category in self.categories:
            md += f"#{category.replace(' ', '-')} "
        md += "\n\n"

        md += f"Post date: {self.post_date}\n"
        md += f"Post modified: {self.post_modified}\n\n"

        md += f"{self.content}"

        return md


@dataclass
class Blog:
    title: str
    description: str
    url: str
    posts: list[Post]

    def from_file(input: Path):
        tree = ElementTree.parse(input)

        # The root of WXR is an <rss> element, followed by a <channel> element
        channel = tree.getroot().find("channel")

        title = channel.find("title").text
        description = channel.find("description").text
        url = channel.find("link").text
        posts = [
            Post.from_element(e)
            for e in channel.findall("item")
            if e.find("wp:post_type", NAMESPACES).text in ["post", "page"]
        ]

        return Blog(title=title, description=description, url=url, posts=posts)


if __name__ == "__main__":
    blog = Blog.from_file(Path(sys.argv[1]))

    out_dir = DEFAULT_OUTPUT_FOLDER / blog.title
    out_dir.mkdir(exist_ok=True, parents=True)

    for post in blog.posts:
        file = out_dir / f"{post.id}-{post.name}.md"
        file.write_text(post.to_md())
