# valimdep

```shell
valimdep ../jwst --ignore-path tests --ignore-path docs --ignore-path jwst/regtest --show-import-paths
```
```
[jwst] found 5 package dependencies not explicitly imported
drizzle
pyparsing
scikit_image
packaging
importlib_metadata
[jwst] found 3 explicit imports not listed in package dependencies
yaml ['jwst/associations/association_io.py']
progress ['jwst/lib/progress.py']
pysiaf ['jwst/lib/siafdb.py']
```
