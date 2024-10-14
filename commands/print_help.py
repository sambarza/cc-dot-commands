from cat.looking_glass.stray_cat import StrayCat


def print_help(cat: StrayCat):

    commands = """
**`Dot Commands`**
```
```

*`Quick resend`*
```text
[.r]      - Resend the last question
[.r nnn]  - Resend a specific HUMAN question
```

*`History manipulation`*
```text
[.ph]     - Print chat History
[.rt]     - Remove last Turn
[.ch]     - Clear chat History
[.ch nnn] - Clear chat History after nnn
[.sh]     - Save chat History (not implemented)
[.lh]     - Load chat History (not implemented)
```

*```"Why" of last answer```*
```text
[.lw]     - Print last "why" formatted
[.lwr]    - Print last "why" in raw format
```
*`Plugins management`*
```text
[.lp]     - List installed plugins
```

*`Sessions management`*
```text
[.whoami] - Print current user
[.as]     - Print active sessions
[.cs]     - Clear all sessions (cannot close ws sessions??)
```

*`Cat internals`*
```text
[.ti]     - Thread Infos
[.st nnn] - Sleep thread for nnn seconds (block thread event loop)
```

"""

    return {"output": commands}
