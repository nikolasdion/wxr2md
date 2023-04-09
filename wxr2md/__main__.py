#!/usr/bin/env python3

import sys
from pathlib import Path

from wxr2md.lib import Blog

DEFAULT_OUTPUT_FOLDER: Path = Path("./out")


if __name__ == "__main__":
    blog = Blog.from_file(Path(sys.argv[1]))

    out_dir = DEFAULT_OUTPUT_FOLDER / blog.title
    out_dir.mkdir(exist_ok=True, parents=True)

    for post in blog.posts:
        if post.is_draft:
            filename = f"draft-{post.id}-{post.name}.md"
        else:
            filename = f"{post.post_date.date()}-{post.name}.md"
        file = out_dir / filename
        file.write_text(post.to_md())
