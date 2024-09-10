# Dot Commands

[![awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=awesome+plugin&color=383938&style=for-the-badge&logo=cheshire_cat_ai)](https://)  
[![Awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=Awesome+plugin&color=000000&style=for-the-badge&logo=cheshire_cat_ai)](https://)  
[![awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=awesome+plugin&color=F4F4F5&style=for-the-badge&logo=cheshire_cat_black)](https://)

Introducing the Cheshire Cat AI `dot commands` plugin, a handy utility designed to simplify and speed up your plugin development process. This tool allows you to interact with the Cat internals directly through chat commands. No need to switch contexts or break your workflow—just type commands starting with a dot (.) to perform various actions.



**Important**

This plugin uses internal mechanisms of Cheshire Cat that are not publicly released. It is not recommended to use it as an example.

## Usage

After installing the plugin, you can send the `.` command to view a list of all available dot commands.

## Available commands
```
History manipulation
[.ph]     - Print chat History
[.ch]     - Clear chat History
[.rt]     - Remove last Turn
[.kh nnn] - Keep chat History up to nnn turns
[.sh]     - Save chat History (not implemented yet)
[.lh]     - Load chat History (not implemented yet)

Quick resend
[.r]      - Resend the last question
[.r nnn]  - Resend a specific HUMAN question

"Why" of last answer
[.lw]     - Print last "why" formatted
[.lwr]    - Print last "why" in raw format

Plugins management
[.lp]     - List installed plugins

Sessions management
[.whoami] - Print current user
[.as]     - Print active sessions
[.cs]     - Clear all sessions (cannot close ws sessions yet)
```