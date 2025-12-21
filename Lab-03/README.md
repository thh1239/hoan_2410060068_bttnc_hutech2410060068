# Lab-03 - Caesar / RSA / ECC (Fixed)

## 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 2) Run API server (Flask)
```bash
python api.py
```
Server runs at: http://127.0.0.1:5001

### Caesar endpoints
- POST `/api/caesar/encrypt`
```json
{ "plain_text": "HUTECH", "key": 3 }
```
Response:
```json
{ "encrypted_message": "KXWHFK" }
```

- POST `/api/caesar/decrypt`
```json
{ "cipher_text": "KXWHFK", "key": 3 }
```
Response:
```json
{ "decrypted_message": "HUTECH" }
```

## 3) Run Caesar UI
(Open another terminal, keep API running)
```bash
python caesar_cipher.py
```

## Notes
- If you change the API port, update URLs in `caesar_cipher.py`.
