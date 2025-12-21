from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc import ECCCipher

app = Flask(__name__)

rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()

# --------------------
# Caesar Cipher API
# --------------------

def _caesar_transform(text: str, key: int, decrypt: bool = False) -> str:
    """Shift letters by key (supports A-Z / a-z). Non-letters are kept."""
    key = int(key) % 26
    if decrypt:
        key = (-key) % 26

    out = []
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:  # A-Z
            out.append(chr((o - 65 + key) % 26 + 65))
        elif 97 <= o <= 122:  # a-z
            out.append(chr((o - 97 + key) % 26 + 97))
        else:
            out.append(ch)
    return "".join(out)


@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.json or {}
    plain_text = data.get('plain_text', '')
    key = data.get('key', None)

    if key is None or str(key).strip() == '':
        return jsonify({'error': 'Missing key'}), 400

    encrypted = _caesar_transform(plain_text, key, decrypt=False)
    return jsonify({'encrypted_message': encrypted})


@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.json or {}
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', None)

    if key is None or str(key).strip() == '':
        return jsonify({'error': 'Missing key'}), 400

    decrypted = _caesar_transform(cipher_text, key, decrypt=True)
    return jsonify({'decrypted_message': decrypted})


@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type']

    private_key, public_key = rsa_cipher.load_keys()

    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400

    encrypted_message = rsa_cipher.encrypt(message, key)
    encrypted_hex = encrypted_message.hex()
    return jsonify({'encrypted_message': encrypted_hex})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data['ciphertext']
    key_type = data['key_type']

    private_key, public_key = rsa_cipher.load_keys()

    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'}), 400

    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']

    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']

    _, public_key = rsa_cipher.load_keys()

    signature = bytes.fromhex(signature_hex)
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    _, public_key = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)