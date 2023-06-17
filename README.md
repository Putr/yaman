# yaman - Yakuake terminal manager

Manager for [Yakuake](https://apps.kde.org/sl/yakuake/), a drop-down, tabbed & tiled terminal emulator.

## What?

You know how working on a project you often need, besides an open IDE and browser, a number of separate terminals (npm, git, docker environment, ... ). You also need to run some scripts before you start and after you finish (e.g. docker containers). It's a hassle, right? Everything just becomes a nightmare when working on multiple projects.

Well, no more. Now you can setup your project environment with a single command.

### What isn't covered?

The only thing I have not figured out how is to automate [Tab Session Manager](https://addons.mozilla.org/en-US/firefox/addon/tab-session-manager/) - i.e. the browser tabs.

Everything else - docker, vscode, yakuake can be handled by this tool.

PS: This is obviously a solution for a very specific set of tools. It's not meant to be a general purpose tool.

## Features

* Define tabs and terminals to open as part of a profile
* Open, close and switch profiles
* Tabs can define custom tiling per tab
* Each created terminal can run any predefined set of commands
* Run predefined commands when opening and when closing a profile (i.e. start/stop dockers)

## How does it work?

You define a profile config file where you define the tabs, how they are split and what commands should be run (cd-ing into folders, tailing logs, starting file watchers, sshing into a server etc.) that looks like this:

    version: 1
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

### Create a new profile

This creates a config file and opens it in your default editor.

    yaman create <profileName>

### List all profiles

    yaman list

### Open a profile

    yaman open <profileName>

### Stop a profile

    yaman close <profileName>

### Switch profile

This will close the open profile(s) and open the specified one.

    yaman switch <profileName>

### Edit profile

    yaman edit <profileName>

## How to install

### Required

You'll need `qdbus` found in the following packages:

* Arch: qt5-tools
* Debian/Ubuntu: qttools5-dev-tools (not tested!)

### Development

    git clone <path>
    poetry install
    poetry run yaman
