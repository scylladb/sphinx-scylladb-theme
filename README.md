# Scylla documentation

This is the repository for [Scylla documentation site](http://docs.scylladb.com/)

To report an issue with the documentation, please use GitHub issues.

This repository accepts GitHub pull requests.

**Send pull requests to the master branch, not gh-pages.  gh-pages will be overwritten by deploy without warning.**


## Prerequisites

* Python 3. Check your verion with `$ python --version`

### Prerequisites: Mac OS X

You must have a working [Homebrew](http://brew.sh/) in order to install the needed tools.

You also need the standard utility `make`.  (I don't know if this comes with Mac OS X.)

Check if you have these two items with

```sh
brew help
make -h
```


### Prerequisites: Fedora 29/Debian-based Linux Distributions

This should work out of the box with Fedora 29

If you do not have the `virtualenv` command installed, you will need `sudo` access, because the setup script has to run one command with sudo.

### Prerequisites: Windows

Use "Bash on Ubuntu on Windows", everything should be same as on a debian-based linux.
Note: livereload seems not working on Windows.

## Prerequistes: other systems

FIXME



# Working on the docs

Work on a task branch and send pull requests for
master.  Master is the default branch.

Run `make preview` to make the docs and preview locally.


# Deploy

If you have the rights to push to the live site, run `make deploy` to deploy.


# Cleanup

You can clean up all the build products and auto-installed Python stuff with:

```sh
make pristine
```

# Contributor info

If you are interested in contributing to Scylla
docs, please read the Scylla open source page at
http://www.scylladb.com/opensource/ and complete
a Scylla contributor agreement if needed.  We can
only accept documentation pull requests if we have
a contributor agreement on file for you


# Third-party documentation

 * Do any copying as a separate commit.  Always commit an unmodified version first and then do any editing in a separate commit.

 * We already have a copy of the Apache license in our tree so you do not need to commit a copy of the license.

 * Include the copyright header from the source file in the edited version.  If you are copying an Apache Cassandra document with no copyright header, use:

```
This document includes material from Apache Cassandra.
Apache Cassandra is Copyright 2009-2014 The Apache Software Foundation.
```
