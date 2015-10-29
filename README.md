# About

[![Build Status](https://travis-ci.org/openaire/vipe.png?branch=master)](https://travis-ci.org/openaire/vipe)


This is a tool for visualizing Apache Oozie pipelines.

# License

The code is licensed under Apache License, Version 2.0

# Dependencies

Python packages that the application depends on are listed in the `requirements.txt` file. Note that:

- The project uses Python 3, so you need to install Python 3 version of these dependencies (on Ubuntu 14.04 system you can do it by executing, e.g. `sudo pip3 install pytest`).
- `pyyaml` package requires `libyaml` library to be installed in the system. On Ubuntu 14.04 system, this can be installed by running `apt-get install libyaml-dev`

# Code development

The **docstrings** in the code follow [Google style guide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Comments) with types declared in accordance to [Sphinx](http://sphinx-doc.org/)'s [type annotating conventions](http://sphinx-doc.org/latest/ext/example_google.html). Note that you have to use Sphinx version at least 1.3 if you want to generate documentation with type annotations.
