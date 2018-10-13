### Sample Flask Application

#### How to read this module.

This project, from an application standpoint, was put together very quickly.  This module is not meant to teach you how to structure a Flask application.  Rather, it exists to show off the capabilities of the router.

There are three modules which have some educational value.  Those have been listed below.

##### components.py

`components.py` demonstrates the structure of a component.  It's purpose is to demonstate when to subclass, when to mixin, and how to decouple behavior.

##### controllers.py

`controllers.py` illustrates how to construct the core of your application.  Application logic can live within the controller or it can be accessed through the handler.

##### routes.py

`routes.py` demonstrates various techniques for registering routes.  This module shows how behavior can be *composed* and how onerous configuration can be abstracted away.
