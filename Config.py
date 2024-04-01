from functools import wraps
from nacl.signing import VerifyKey

class IntType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

class IntRespType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE =  7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        print(ex)
    return False

def verify_key_decorator(client_public_key):
    from flask import request, jsonify

    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            signature = request.headers.get('X-Signature-Ed25519')
            timestamp = request.headers.get('X-Signature-Timestamp')
            if signature is None or timestamp is None or not verify_key(request.data, signature, timestamp, client_public_key):
                return 'Bad request signature', 401

            if request.json and request.json.get('type') == IntType.PING:
                return jsonify({
                    'type': IntRespType.PONG
                })

            return f(*args, **kwargs)
        return __decorator
    return _decorator