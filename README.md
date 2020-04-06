# caesar-cipher-cli

## Install dependencies
```
 pip install click
```

## Run code

### 1. Get challenge json
```
python main.py challenge --token YOUR_TOKEN
```

### 2. Decrypt json message
```
python main.py decrypt answer.json 
```

### 3. Send challenge json
```
python main.py send --token YOUR_TOKEN answer.json 
```
