[![Travis Badge](https://travis-ci.org/tpaviot/pythonocc-demos.svg?branch=master)](https://travis-ci.org/tpaviot/pythonocc-demos)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/2h130pglpchxjd5i/branch/master?svg=true)](https://ci.appveyor.com/project/tpaviot/pythonocc-demos)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tpaviot/pythonocc-demos.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tpaviot/pythonocc-demos/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6a7ad7d29ff44acea40ef5f130249557)](https://www.codacy.com/app/tpaviot/pythonocc-demos?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tpaviot/pythonocc-demos&amp;utm_campaign=Badge_Grade)

Some pythonocc related code snippets, examples, jupter notebooks etc.

Requirements :

* pythonocc-core 7.4.1

````
conda install -c conda-forge pythonocc-core=7.4.1
````

* jupyter if you want to test the jupyter notebooks, as well as pythreejs.

Repository structure :

* assets: 2D images, 3D modules in various formats. Used by the python scripts

* examples: small python scripts that each describe a pythonocc feature
```
    $ cd examples  
    $ python core_helloworld.py
```

* jupyter_notebook: a set of examples running pythonocc inside a jupyter notebook.
```
    $ cd jupyter_notebooks  
    $ jupyter notebook
```
