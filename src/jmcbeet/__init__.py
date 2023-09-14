"""
Plugin for integrating JMC into beet.

To install JMC, run `pip install jmcfunction --pre`

Setup in beet.yml:
```yml
meta:
  jmc:
    namespace: my_namespace
    file: src/data/my_namespace/jmc/main.jmc
```
You can also modify jmc.txt content virtually with beet.yml, though, it's optional
```yml
meta:
  jmc:
    namespace: my_namespace
    file: src/data/my_namespace/jmc/main.jmc
    LOAD: __load__
    TICK: __tick__
    PRIVATE: __private__
    VAR: __variable__
    INT: __int__
    STORAGE: __storage__
```
"""
from typing import Callable, Any
from beet import (
    Advancement,
    BlockTag,
    Context,
    DataPack,
    EntityTypeTag,
    FluidTag,
    Function,
    FunctionTag,
    GameEventTag,
    ItemModifier,
    ItemTag,
    LootTable,
    Predicate,
    Recipe
)

from .config import VERSION

RESOURCE_TYPE_MAP: dict[str, Callable[[str], Any]] = {
    "tags/block": BlockTag,
    "tags/entity_types": EntityTypeTag,
    "tags/fluids": FluidTag,
    "tags/functions": FunctionTag,
    "tags/game_events": GameEventTag,
    "tags/items": ItemTag,
    "advancements": Advancement,
    "functions": Function,
    "item_modifiers": ItemModifier,
    "loot_tables": LootTable,
    "predicates": Predicate,
    "recipes": Recipe
}

DEFAULT_JMC_TXT = {
    "LOAD": "__load__",
    "TICK": "__tick__",
    "PRIVATE": "__private__",
    "VAR": "__variable__",
    "INT": "__int__",
    "STORAGE": "__storage__"
}


def beet_default(ctx: Context):
    try:
        from jmc.api import PyJMC, EXCEPTIONS as JMC_EXCEPTIONS
    except ImportError:
        print("JMC-Warning | JMC is not installed. ")
        return

    datapack = DataPack()
    if "jmc" not in ctx.meta:
        print("JMC-Warning | meta.jmc is not specified in beet.yml")
        return
    if "namespace" not in ctx.meta["jmc"]:
        print("JMC-Warning | meta.jmc.namespace is not specified in beet.yml")
        return
    if "file" not in ctx.meta["jmc"]:
        print("JMC-Warning | meta.jmc.file is not specified in beet.yml")
        return
    namespace: str = ctx.meta["jmc"]["namespace"]
    file_path: str = ctx.meta["jmc"]["file"]

    jmc_txt = {}
    for key, value in DEFAULT_JMC_TXT.items():
        jmc_txt[key] = ctx.meta["jmc"].get(key, value)

    try:
        jmc_pack = PyJMC(
            namespace,
            description="",
            pack_format="-1",
            target=file_path,
            jmc_txt=jmc_txt)
    except JMC_EXCEPTIONS as error:
        print("JMC-Warning | JMC Error has occured")
        print(type(error).__name__)
        print(error)
        return
    except Exception as error:
        print("JMC-Warning | Unknown exception has occured. This is an error in JMC, not beet's fault.")
        print(type(error).__name__)
        print(error)
        return

    for resource in jmc_pack.resource_locations:
        if resource.type not in RESOURCE_TYPE_MAP:
            print(
                f"JMC-Warning | Unrecogized resource type '{resource.type}'. Couldn't add '{resource.location}'")
            continue
        datapack[resource.location] = RESOURCE_TYPE_MAP[resource.type](
            resource.content)

    ctx.data.merge(datapack)
