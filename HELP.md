#### One of my application's views doesn't fit nicely into my routing structure.

Flask-router doesn't need to be used for every route. Special cases may require you to define the url rule directly. To do this follow these steps:

1. Locate in your application where URL rules are defined.
2. Access the flask application used in that context.
3. Call the `app.add_url_rule` method directly.
    * Documentation for this method can be found on the flask website.

#### One or more of my components don't seem to be working.

Check the ordering of your components. Components that appear first in a list or in a higher node of the tree will be called first. Go through your components, in order, and make sure each of them makes a call to their parent and returns its result. For example:

```python
def my_method(self):
    result = self.parent.my_method()
    result['my_mutation'] = True
    return result
```

#### I can't get my components to control the application the way I want.

Consider that "components" and "middleware" only decorate behavior. They don't control it. "Controllers" control application behavior. Adding new controllers or rewriting your existing controllers may be a better use of your time.