# Plutus - Discord tip bot on Fantom Opera

## Setup

1. Install Python 3.9 or higher

2. Install sqlite3 if it's not installed

3. Install pipenv

```
pip3 install pipenv
```

4. Clone the repo and *cd* into its root

5. Install the dependencies

```
pipenv install
```

6. Generate a new secret key (needed for step 6). **IMPORTANT: DON'T SHARE THIS
   KEY WITH ANYONE!**

```
pipenv run python generate_secret_key.py
```

7. On the folder `local` create the files `default.env` and `secrets.env` and
fill in the missing variables following the example files.

8. Run the bot

```
pipenv run python main.py
```
