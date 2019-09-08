# Tman - Terminal manager

Terminal manager used to control tabbed tiled terminals with current support for Yakuake and Guake.

## Terminal support

* Yakuake
* Gauke (planned)

## Features

* Define tabs and terminals to open as part of a profile
* Open, close and switch profiles
* Tabs can define custom tiling per tab
* Each created terminal can run any predefined set of commands
* Run predefined commands when opening and when closing a profile
* Support multiple terminals with the same config (planned)
* Modify size of tiled terminals (planned)

## Why?

Do you find yourself constantly opening the same tabs, runing the same commands all just to setup your "optimal" work enviroment? Do you hate the fact that these tabbed terminals are missing session saving? Do you hate changing your terminal setup when switching between projects?
Well, so do I.

## How does it work?

You define a profile config file where you define the tabs, how they are split and what commands should be run (cd-ing into folders, tailing logs, starting file watchers, sshing into a server etc.) that looks like this:

    version: 1
    terminal: yakuake
    variables:
      path: /your/path 
    pre:
      - cd %path%
      - docker-compose start
    tabs:
      yourTabName: 
        - "cd %path%"
        - "git status"
      htop:
        - "htop"
      splitTab:
        left:
          top:
            - "ls -la"
          bottom: 
            - "ll"
        right:
          - "ps faux"
      server:
        - ssh server
    down:
      - cd %path%
      - docker-compose stop

## How do I use it?

**Create a new profile**
This creates a config file and opens it in your default editor.

    tman create <profileName>

**Start a profile**

    tman start <profileName>

**Stop profile**

    tman close <profileName>

**Switch profile**
This will close the open profile(s) and open the specified one.

    tman switch <profileName>

**Edit profile**

    tman edit <profileName>

## How to install

    git clone <path>
    virtualenv venv
    . venv/bin/activate
    pip install --editable .

