#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

from wxr2md.lib import Blog


def main(input_file: Path, out_dir: Path) -> None:
    blog = Blog.from_file(input_file)

    out_dir = out_dir / blog.title
    out_dir.mkdir(exist_ok=True, parents=True)

    for post in blog.posts:
        if post.is_draft:
            filename = f"draft-{post.id}-{post.name}.md"
        else:
            filename = f"{post.post_date.date()}-{post.name}.md"
        file = out_dir / filename
        file.write_text(post.to_md())


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="wxr2md",
        description="Convert WordPress eXport RSS (WXR) into Markdown files",
    )
    parser.add_argument("input")
    parser.add_argument(
        "--out",
        help="output directory, defaults to 'out/' in the current working directory",
        default="./out",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out)

    main(input_path, out_dir)
