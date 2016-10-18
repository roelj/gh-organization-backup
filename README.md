# gh-organization-backup

This repository contains a single script to backup your organization's
repositories from GitHub.  Before you can use it, you need to do three things:

1. Install [PyGithub](https://pypi.org/project/PyGithub/)
2. Install [Git](https://git-scm.com/)
2. Configure the following variables inside `ghbackup.py`:
```{python}
##
## Specify a Github access token.
##
## 1. Go to https://github.com/settings/tokens
## 2. Generate a token with "read:org" and "repo" permissions.
## 3. Paste the token as a string below.
##
token            = ""

##
## Specify the name of the organization you would like to back-up.
##
organization     = ""

##
## Specify the log directory and the target directory to place
## the repository back-ups.
##
target_directory = ""
log_directory    = ""
```
