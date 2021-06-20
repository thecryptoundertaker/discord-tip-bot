# Dev Setup

First clone the repo, then create a python virtual environment:

```
python -m venv venv
```

Enter the python virtual environment:

Bash:
```
source venv/bin/activate
```
Fish:
```
source venv/bin/activate.fish
```
CSH:
```
source venv/bin/activate.csh
```

Upgrade the python package manager pip and install the wheel package for binary packages:
```
pip install pip --upgrade
pip install wheel
```

Install the required 3rd party dependencies:
```
pip install -r requirements.txt
```

Run the main app:
```
python tippy.py
```


