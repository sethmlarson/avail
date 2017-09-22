# Avail

A small tool I made when I was tired of searching for if a name was available in a bunch of places.

As we know, naming is the hardest part of programming. Avail speeds that process up a little bit.

## Usage

Install with `pip`. Run via `python -m avail [NAME]` or `avail [NAME]`.
You will see colors in the terminal as to whether the given name is available.

```bash
bash-4.4$ python -m pip install avail
bash-4.4$ python -m avail name
dev
 - [?] bitbucket
 - [N] github
 - [?] gitlab
package
 - [?] cargo
 - [?] npm
 - [Y] pypi
 - [N] rubygems
social
 - [?] dribble
 - [?] mastodon.social
 - [?] tumblr
 - [?] twitter
web
 - [N] name.com
 - [Y] name.io
 - [N] name.me
 - [N] name.net
 - [N] name.org
 - [N] na.me
```

## Contributing
 
Pull Requests as welcome! This is a small project that is made only to suit my own needs.
If you want to expand it to check more services feel free to add them.
 
## License
 
Avail is licensed under Apache-2.0.
 
