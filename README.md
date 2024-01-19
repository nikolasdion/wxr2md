# wxr2md - Convert WXR Files into Markdown

Convert WordPress exPort RSS (WXR) files to Markdown files with YAML frontmatter.

## Installation

Install using pip,

```sh
pip install wxr2md
```

## Usage

```
usage: wxr2md [-h] [--output OUTPUT] [--no-frontmatter] [--title-in-body] [--date-in-body] input

Convert WordPress eXport RSS (WXR) into Markdown files

positional arguments:
  input             path to the WXR file to be converted

options:
  -h, --help        show this help message and exit
  --output OUTPUT   output directory, defaults to 'out/' in the current working directory
  --no-frontmatter  don't add YAML frontmatter to the markdown file
  --title-in-body   add title in the markdown body as an h1 element
  --date-in-body    print date at the start of the markdown body
```

## Output

By default, the script will output to `out/` folder in the current working directory.

The markdown file output is as follows. The frontmatter mostly follows the frontmatter properties of [Hugo](https://gohugo.io/), except for `id`.

```markdown
---
id: 1
title: Hello, world!
type: post
date: 1970-01-01 12:34:56
lastmod: 1980-02-02 01:02:03
categories:
  - a category
  - another category
tags:
  - my tag
  - your tag
draft: true
---

# Hello, world! <!-- If passing in --title-in-body argument -->

_Mon 01 Jan 1970, 12:34_ <!-- If passing in --date-in-body argument -->

This is the content of the blog post. Perhaps there are a few sentences here.
```

## Limitations:

- only tested with WXR version 1.2 and a limited set of exports, so might not be compatible for all WXR files
- `date` and `lastmod` is in local timezone and does not include timezone data
- blog information is not outputed anywhere (e.g. description, url, etc.)
- no option to customise the output file names and folder structures

## Building

This package uses [poetry](https://python-poetry.org/) for dependency management and packaging. See their documentation for setup and usage.
