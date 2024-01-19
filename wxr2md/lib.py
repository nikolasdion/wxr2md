from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

from markdownify import markdownify
from yaml import dump

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

    id: int
    """Unique ID of the post"""
    type: str
    """Type of blog entry, e.g. page or post"""
    title: str
    """Title of the post as displayed in the page, can be None"""
    name: str
    """Name in the URL of the post"""
    content: str
    """Content, in markdown format"""
    date: datetime
    """Date posted, from wordpress metadata"""
    modified: datetime
    """Date last modified, from wordpress metadata"""
    categories: list[str]
    """List of categories this post is associated with"""
    tags: list[str]
    """List of tags this post is associated with"""
    draft: bool
    """Whether this post is a draft"""

    DATE_IN_BODY_FORMAT = "%a %d %b %Y, %I:%M"

    @classmethod
    def from_element(cls, element: ElementTree.Element):
        """Create a post from an XML element"""
        title = element.find("title").text
        name = element.find("wp:post_name", NAMESPACES).text
        id = int(element.find("wp:post_id", NAMESPACES).text)
        type = element.find("wp:post_type", NAMESPACES).text

        content = element.find("content:encoded", NAMESPACES).text
        if content is not None:
            content = markdownify(content)

        try:
            date = datetime.fromisoformat(element.find("wp:post_date", NAMESPACES).text)
        except ValueError:
            date = None

        try:
            modified = datetime.fromisoformat(
                element.find("wp:post_modified", NAMESPACES).text
            )
        except ValueError:
            modified = None

        categories =  [e.text for e in element.findall("category") if e.get("domain") == "category"]
        tags =  [e.text for e in element.findall("category") if e.get("domain") == "post_tag"]

        draft = element.find("wp:status", NAMESPACES).text == "draft"

        return cls(
            title=title,
            name=name,
            id=id,
            type=type,
            content=content,
            date=date,
            modified=modified,
            categories=categories,
            tags=tags,
            draft=draft,
        )

    def get_frontmatter(self) -> str:
        """Generate YAML frontmatter"""

        frontmatter = {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "date": self.date,
            "modified": self.modified,
            # "categories": self.categories,
            # "tags": self.tags,
            # "draft": self. draft
        }

        if len(self.categories) > 0:
            frontmatter["categories"] = self.categories
        
        if len(self.tags) > 0:
            frontmatter["categories"] = self.tags

        if self.draft:
            frontmatter["draft"] = self.draft

        return dump(frontmatter, sort_keys=False)

    def md_body(self, include_title=False, include_date=False) -> str:
        """Generate markdown text body lines"""
        lines = []
        if self.title is not None and include_title:
            lines.append(f"# {self.title}")
            lines.append("")
        if self.date is not None and include_date:
            lines.append(f"_{self.date.strftime(self.DATE_IN_BODY_FORMAT)}_")
            lines.append("")
        if self.content is not None:
            lines.append(f"{self.content}")
            lines.append("")
        return "\n".join(lines)

    def to_md(
        self,
        frontmatter=True,
        title_in_body=True,
        date_in_body=True,
    ) -> str:
        """Convert post into a markdown string"""
        md = ""
        if frontmatter:
            md += "---\n"
            md += self.get_frontmatter()
            md += "---\n\n"
        md += self.md_body(title_in_body, date_in_body)
        return md


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
