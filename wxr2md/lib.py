from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

from markdownify import markdownify

NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


@dataclass
class Post:
    """Represents a WordPress blogpost"""

    id: str
    """Unique ID of the post"""
    title: str
    """Title of the post as displayed in the page, can be None"""
    name: str
    """Name in the URL of the post"""
    content: str
    """Content, in markdown format"""
    pub_date: str
    """From pubDate element, RFC 822 format"""
    post_date: datetime
    """From wordpress metadata"""
    post_modified: datetime
    """From wordpress metadata"""
    categories: list[str]
    """List of categories/tags this post is associated with"""
    is_draft: bool

    @classmethod
    def from_element(cls, element: ElementTree.Element):
        """Create a post from an XML element"""
        title = element.find("title").text
        name = element.find("wp:post_name", NAMESPACES).text
        id = element.find("wp:post_id", NAMESPACES).text
        content = element.find("content:encoded", NAMESPACES).text
        if content is not None:
            content = markdownify(content)

        pub_date = element.find("pubDate", NAMESPACES).text

        try:
            post_date = datetime.fromisoformat(
                element.find("wp:post_date", NAMESPACES).text
            )
        except ValueError:
            post_date = None

        try:
            post_modified = datetime.fromisoformat(
                element.find("wp:post_modified", NAMESPACES).text
            )
        except ValueError:
            post_modified = None

        categories = [e.text for e in element.findall("category")]
        is_draft = element.find("wp:status", NAMESPACES).text == "draft"

        return cls(
            title=title,
            name=name,
            id=id,
            content=content,
            pub_date=pub_date,
            post_date=post_date,
            post_modified=post_modified,
            categories=categories,
            is_draft=is_draft,
        )

    def md_metadata(self) -> str:
        """Generate YAML metadata lines to be included in the markdown string"""
        lines = []
        lines.append("---")
        lines.append(f"id: {self.id}")
        lines.append(f"title: {self.title}")
        lines.append(f"post_date: {self.post_date}")
        lines.append(f"post_modified: {self.post_modified}")
        lines.append(f"categories: {self.categories}")
        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def md_body(self) -> str:
        """Generate markdown text body lines"""
        lines = []
        if self.title is not None:
            lines.append(f"# {self.title}")
            lines.append("")
        if self.pub_date is not None:
            lines.append(f"_{self.pub_date}_")
            lines.append("")
        if self.content is not None:
            lines.append(f"{self.content}")
            lines.append("")
        return "\n".join(lines)

    def to_md(self) -> str:
        """Convert post into a markdown string"""
        metadata = self.md_metadata()
        body = self.md_body()

        return metadata + "\n" + body


@dataclass
class Blog:
    """Represents a WordPress blog"""

    title: str
    """Title of the blog, as displayed in the webpage"""
    description: str
    """Description of the blog, as displayed in the webpage"""
    url: str
    """URL of the blog"""
    posts: list[Post]
    """List of posts and pages in the blog, including drafts"""

    @classmethod
    def from_file(cls, input: Path):
        """Create a Blog object from a WXR file"""
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

        return cls(title=title, description=description, url=url, posts=posts)
