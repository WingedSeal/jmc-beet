# jmc-beet

Plugin for integrating JMC into beet.

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