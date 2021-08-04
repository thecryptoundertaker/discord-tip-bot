# Plutus - Discord tip bot on Fantom Opera

## Setup (using Docker)

1. Install Docker

2. Clone the repo and *cd* into its root

3. Build the docker image

```bash
docker build --tag plutus-key .
```

5. Generate a new secret key (needed for step 6). **IMPORTANT: DON'T SHARE THIS
   KEY WITH ANYONE!**

    1. Create a container and get inside of it

    ```bash
    docker run -it plutus-key /bin/bash
    ```

    2. Generate secret key

    ```bash
    pipenv run python3 generate_secret_key.py
    ```

    3. Save the secret key

    4. Exit the container

    ```bash
    exit
    ```

6. On the folder `local` create the files `default.env` and `secrets.env` and
fill in the missing variables following the example files.

7. Recreate a docker image with env variables all set

```bash
docker build --tag plutus-main .
```

7. Run the container with the env variables all set

```bash
docker run -it -d plutus-main pipenv run python3 main.py
```

## Setup (without Docker)

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
