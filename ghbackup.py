# Copyright (C) 2016  Roel Janssen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import datetime
import json

from github import Github
from github import GithubException
from github import BadCredentialsException
from github import UnknownObjectException

## ----------------------------------------------------------------------------
## BEGIN OF CONFIGURATION
## ----------------------------------------------------------------------------

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

## ----------------------------------------------------------------------------
## END OF CONFIGURATION
## ----------------------------------------------------------------------------

try:
    gh_connection    = Github(token)
    gh_organization  = gh_connection.get_organization(organization)

except BadCredentialsException as e:
    print("Your access token seems to be invalid.")

except UnknownObjectException as e:
    print("The Github API seems to have changed.  This scripts needs" +
          " adjustments.")

except GithubException as e:
    print("Something went wrong, but we don't know what.")
    print("Here's the raw data (you're on your own):\n" + json.dumps(e.data))

else:
    timestamp        = datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S")
    pull_log         = log_directory + "/pull-" + timestamp + ".log"
    clone_log        = log_directory + "/clone-" + timestamp + ".log"

    print("Updating/cloning repositories:")

    for repo in gh_organization.get_repos():
        print(" * " + repo.name)
        repo_dir = target_directory + "/" + repo.name

        ## When we already have a backup, only pull updates.
        if os.path.exists(repo_dir):
            os.chdir(repo_dir)

            ## Pull everything so we have a complete backup.  Without the
            ## '--all' argument, we may only have the 'master' branch.
            os.system("git pull --all >> " + pull_log + " 2>&1")

        ## Clone repositories we haven't backed up yet.
        else:
            os.system("git clone https://github.com/" +
                      organization + "/" + repo.name + ".git " +
                      target_directory + "/" + repo.name + " >> " +
                      clone_log + " 2>&1")
