#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

from wxr2md.lib import Blog


def main(
    input_file: Path,
    out_dir: Path,
    no_frontmatter=True,
    title_as_header=False,
    date_in_body=False,
) -> None:
    blog = Blog.from_file(input_file)

    out_dir = out_dir / blog.title

    posts_dir = out_dir / "posts"
    posts_dir.mkdir(exist_ok=True, parents=True)

    drafts_dir = out_dir / "drafts"
    drafts_dir.mkdir(exist_ok=True, parents=True)

    for post in blog.posts:
        if post.is_draft:
            file = drafts_dir / f"{post.id}.md"
        else:
            file = posts_dir / f"{post.post_date.date()}-{post.name}.md"

        file.write_text(
            post.to_md(
                frontmatter=not no_frontmatter,
                title_in_body=title_as_header,
                date_in_body=date_in_body,
            )
        )


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="wxr2md",
        description="Convert WordPress eXport RSS (WXR) into Markdown files",
    )
    parser.add_argument("input", help="path to the WXR file to be converted")
    parser.add_argument(
        "--output",
        help="output directory, defaults to 'out/' in the current working directory",
        default="./out",
    )
    parser.add_argument(
        "--no-frontmatter",
        help="don't add YAML frontmatter to the markdown file",
        action="store_true",
    )
    parser.add_argument(
        "--title-in-body",
        help="add title in the markdown body as an Header element",
        action="store_true",
    )
    parser.add_argument(
        "--date-in-body",
        help="print date at the start of the markdown body",
        action="store_true",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.output)

    main(
        input_path,
        out_dir,
        args.no_frontmatter,
        args.title_in_body,
        args.date_in_body,
    )
