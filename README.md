# valimdep: VALidate IMports and DEPendencies

Your Python package's dependencies should ONLY be those packages that you EXPLICITLY import and use in your code, and vice versa.
`valimdep` scans your Python package to find explicit imports, then reads the dependencies defined in your project metadata, and gives you a diff between the two lists.

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
