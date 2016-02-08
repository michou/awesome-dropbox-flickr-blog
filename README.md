Bottle on OpenShift
===================

This git repository helps you get up and running quickly w/ a Bottle installation
on the Red Hat OpenShift PaaS.


Running on OpenShift
--------------------

Create an account at https://www.openshift.com/

Create a python application based on the code in this repository

    rhc app create bottle python-2.6 --from-code https://github.com/openshift-quickstart/bottle-openshift-quickstart.git

That's it, you can now checkout your application at:

    http://bottle-$yournamespace.rhcloud.com

Customizing your new app
------------------------

If you don't like your application code to be stored in `myapplication.py` (I know I wouldn't), you can rename `myapplication.py` to whatever you like, but you must also update the module name used in both `wsgi/local.py` and `wsgi/application`.

Do note, that no matter how you choose to name the module your application code resides in, or the name of the application variable, the application must be imported as `application` in `wsgi/application`. For instance:

```python
# This is the `wsgi/application` file

# ...
from myAwesome_app import RockstarNinja as application
```