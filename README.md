**Activate Virtual Environment**

```
source blockchain-env/bin/activate
```

**Install all Packages**

```
pip3 install -r requirements.txt
```

**Run Tests**
```
python3 -m pytest backend/tests
```

**Run API**
```
python3 -m backend.app
```

**Run a PEER instance**
```
export PEER=True && python3 -m backend.app
```