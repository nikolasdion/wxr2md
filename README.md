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

Limitations:

- only tested with WXR version 1.2 and a limited set of exports, so might not be compatible for all WXR files
- `post_date` and `post_modified` is in local timezone, but the date in the markdown body seemed like it's in UTC, even though it's not
- authors are not included in metadata
- blog information is not outputed anywhere (e.g. description, url, etc)
- no option to customise the format of markdown or file name

## Building

This package uses [poetry](https://python-poetry.org/) for dependency management and packaging. See their documentation for setup and usage.
