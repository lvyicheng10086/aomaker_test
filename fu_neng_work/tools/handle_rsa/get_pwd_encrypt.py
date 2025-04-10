import rsa
import base64


def get_encrypted_password(msg:str) -> str:
    """加密文本进行编码"""
    server_pub_key = """
       -----BEGIN PUBLIC KEY-----
       MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCg3E2ExuKTX3phT0
       /F39CbzXF3d8/v8a3Hlajnjk8RsYrwwHXeDLmWMmEgWa1fRwq6oCxoo
       Po1K+RBseh/nDXI3VF4MYpeDs7EJpRHxZ9I9PSNWgiboSvX3w7NIONT
       51eTSeUYid7rwK/UCvH87nGGMyuXo2cuxgKyyaQwwa8fkwIDAQAB
       -----END PUBLIC KEY-----
                    """
    pub_key_byte = server_pub_key.encode("utf-8")
    pub_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)
    content = msg.encode("utf-8")
    cryto_msg = rsa.encrypt(content, pub_key_obj)
    cipher_base64 = base64.b64encode(cryto_msg)
    crypto_data = cipher_base64.decode()
    return crypto_data