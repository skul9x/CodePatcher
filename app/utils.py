import os
import ast
import base64
import hashlib

class TokenCipher:
    @staticmethod
    def _get_key():
        salt = b'TCO_PatchApplier_Secure_Salt_v3.1'
        return hashlib.sha256(salt).digest()

    @staticmethod
    def encrypt(raw_text):
        if not raw_text: return ""
        try:
            key = TokenCipher._get_key()
            enc = bytearray()
            for i, char in enumerate(raw_text.encode('utf-8')):
                enc.append(char ^ key[i % len(key)])
            return base64.b64encode(enc).decode('utf-8')
        except Exception:
            return ""

    @staticmethod
    def decrypt(enc_text):
        if not enc_text: return ""
        try:
            enc_bytes = base64.b64decode(enc_text.encode('utf-8'))
            key = TokenCipher._get_key()
            dec = bytearray()
            for i, b in enumerate(enc_bytes):
                dec.append(b ^ key[i % len(key)])
            return dec.decode('utf-8')
        except Exception:
            return ""

def is_safe_path(base_dir, file_path):
    try:
        # Dùng realpath để resolve symlinks, ngăn chặn symlink bypass attack
        full_path = os.path.realpath(os.path.join(base_dir, file_path))
        base_abs = os.path.realpath(base_dir)
        return os.path.commonpath([base_abs, full_path]) == base_abs
    except Exception:
        return False

def check_syntax(content, filename="<string>"):
    if not filename.endswith(".py"):
        return True, ""
    try:
        ast.parse(content, filename=filename)
        return True, ""
    except SyntaxError as e:
        return False, f"Lỗi cú pháp dòng {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)