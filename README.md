#Epic Events OC- P12

## Info

This project is to create a secure application related to employee, client, contract and events for Epic Events.

The main models are:
- Employee
- Client
- Contract
- Event

There are permissions related to each model which define the action they can take. In general these follow basic CRUD actions:
- Create
- Read
- Update
- Delete


## Installation

1. Initialize the project

Windows :

   ```
    git clone https://github.com/Maiphuongthao/MaiPhuongThao_10_062023.git

    cd MaiPhuongThao_10_062023
    python -m venv env 
    env\scripts\activate

    pip install -r requirements.txt

  ```

MacOS et Linux :

  ```
    git clone https://github.com/Maiphuongthao/MaiPhuongThao_10_062023.git

    cd MaiPhuongThao_10_062023
    python3 -m venv env 
    source env/bin/activate

    pip install -r requirements.txt

  ```

2. Database

   - Install MySQL following their instrucion [Here]([https://www.postman.com/](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
   - ```mysql -u root -p ```then create epic_events database ```CREATE epic_events```

3. Secret information

   - Add .ssh folder ```mkdir .ssh``` then add secret file to the folder ```cd .ssh``` ```touch secret.txt```
   - In the commande line write ```ssh-keygen -t rsa```to generate rsa pair key then go back to main directory```cd ...```
   - In main directory create .env file ```touch .env```. Add all lines from .env-example to .env file. Please change the information following the note of each line.


## Launch the app

To secure the application, it's needed to authenticate with email and password. This will generate a token which expires after 24h.
This application is designed with basic employees, events, contracts to start. The databases is needed to have permission identified included

To start the app:

```python main.py```

To start login

```python main.py login```

To start after login in:

```python main.py start```

To logout:

```python main.py logout```

The basic employees added to database are:

| #   | email              | Password    |
|-----|--------------------|-------------|
| 1   | lucie@test.com     | Pasword12@  |
| 2   | ben@test.com       | Pasword12@  |
| 3   | lao@test.com       | Pasword12@  |

