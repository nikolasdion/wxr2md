# wxr2md - Convert WXR Files into Markdown

Convert WordPress exPort RSS (WXR) files to Markdown files.

## Usage

```sh
wxr2md /path/to/wxr/file [--out /path/to/output/folder]
```

By default, this will output to `out/` folder in the current working directory.

The markdown file output is as follows:

```markdown
---
id: 1
title: Hello, world!
post_date: 1970-01-01 12:34:56
post_modified: 1980-02-02 01:02:03
categories: ["a category", "another category"]
---

# Hello, world!

_Mon, 01 Jan 1970 12:34:56 +0000_

This is the content of the blog post.
```

## Building

This package uses [poetry](https://python-poetry.org/) for dependency management and packaging. See their documentation for setup and usage.
