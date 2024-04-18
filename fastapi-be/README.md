# Testing the websockets
Open three terminals, all in the same directory

## Terminal 1
```
python3 -m venv venv
. ./venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt

docker compose up --build
```

## Terminal 2
```
. ./venv/bin/activate
python recv.py
```

## Terminal 3
```
. ./venv/bin/activate
python send.py
```
