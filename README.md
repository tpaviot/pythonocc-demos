[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6a7ad7d29ff44acea40ef5f130249557)](https://www.codacy.com/gh/tpaviot/pythonocc-demos/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tpaviot/pythonocc-demos&amp;utm_campaign=Badge_Grade)

Some pythonocc related code snippets, examples, jupter notebooks etc.

Requirements :

* pythonocc-core 7.8.1

````
conda install -c conda-forge pythonocc-core=7.8.1
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
