## Sample Implementation

#### Installation

```bash
$ pip install -r requirements.txt
```

#### Run Server

```bash
$ # tty1
$ python examples/app/run.py

$ # tty2
$ curl localhost:5000/v1/users/1/emails
$ curl localhost:5000/v2/users/1/emails
```

#### How To Read This Module

Those aspects of this application unrelated to `flask-compose` were put together with little care. A selection of files which should be considered when introducing yourself to the library have been listed below:

1. components.py
2. controllers.py
3. routes.py

The remaining files can be studied to understand the context in which the above files operate. But ultimately, those files are outside the scope of this application and were paid little mind.
