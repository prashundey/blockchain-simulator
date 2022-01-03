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

**Run Root Instance API**
```
python3 -m backend.app
```

**Run a PEER Instance API**
```
export PEER=True && python3 -m backend.app
```

**Run Instance with Seeded Data**
```
export SEED_DATA=True && python3 -m backend.app
```