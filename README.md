# wxr2md - Convert WXR Files into Markdown

This package uses [poetry](https://python-poetry.org/) for dependency management and packaging.

To build,

```sh
poetry install

poetry build
```

To run,

```sh
python3 wxr2md path/to/wxr/file

# or in poetry environment
poetry run python wxr2md path/to/wxr/file
```

This will output to an `out/` folder from the current working directory.

The output format is specific for my own personal use case at the moment:

```markdown
---
id: 1
title: Hello, world!
...

---

# Hello, world!

This is the content of the blog post.
```
