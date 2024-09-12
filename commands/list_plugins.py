from cat.looking_glass.stray_cat import StrayCat


def list_plugins(cat: StrayCat):

    active_plugins_count = 0
    inactive_plugins_count = 0

    for plugin in cat.mad_hatter.plugins.values():

        if plugin.id == "core_plugin":
            continue

        if plugin.active:
            active_plugins_count += 1
        else:
            inactive_plugins_count += 1

        output = f"""
**`{plugin.id}:  {"active" if plugin.active else "not active"}`**
"""
        if len(plugin.tools) > 0:
            output += """
```
```
**Implemented Tools**
| | |
|-|-|
|`Name` | `Description`| `Return Direct`
"""
            for tool in plugin.tools:
                output += (
                    f"""|`{tool.name}`|`{tool.description}`|{tool.return_direct}\n"""
                )

        if len(plugin.hooks) > 0:
            output += """
```
```
**Used hooks**
|||
|-|-|
|`Name`|`Priority`|
"""

            for hook in plugin.hooks:
                output += f"""|`{hook.name}`|`{hook.priority}`|\n"""

        cat.send_chat_message(output, save=False)

    return {
        "output": f"{active_plugins_count} active plugins / {inactive_plugins_count} inactive plugins"
    }
