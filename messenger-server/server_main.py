import base64

from encrytor import Encryptor
from server import Server
from user import Users
from timeit import default_timer as timer
import hashlib


def test_encryption_time():
    pub_k, pr_k = Encryptor.generate_keys()

    start = timer()
    for i in range(500):
        encrypted = Encryptor.asymmetric_encrypt_message(b'Some stupid message', pub_k)
    end = timer()
    print("500 encryptions time: " + str(end - start))

    encrypted = Encryptor.asymmetric_encrypt_message(b'Some stupid message', pub_k)
    start = timer()
    for i in range(500):
        descripted = Encryptor.asymmetric_decrypt_message(encrypted, pr_k)
    end = timer()
    print("500 decryptions time: " + str(end - start))


def test_hash_time():
    m = hashlib.sha256()
    m.update(b"Nobody inspects")
    start = timer()
    for i in range(10000000):
        m.digest()
    end = timer()
    print("10M hashes time: " + str(end - start))


def generate_new_keys():
    pub_key, pr_key = Encryptor.generate_keys()
    Encryptor.save_public_key(pub_key)
    Encryptor.save_private_key(pr_key)


def main():
    Users.deserialize()
    server = Server('192.168.1.40', 65000)
    server.run()
    Users.serialize()

    # pr_k = Encryptor.load_private_key()
    # pub_k = Encryptor.load_public_key()
    # encrypted = Encryptor.asymmetric_encrypt_message(message=b'fuck it', key=pub_k)
    # print(encrypted)
    # coded = base64.b64encode(encrypted).decode('utf-8')
    # decoded = base64.b64decode(coded)
    # decrypted = Encryptor.asymmetric_decrypt_message(message=decoded, key=pr_k)
    # print(decrypted)

    # test_encryption_time()
    # test_hash_time()
    pass


if __name__ == "__main__":
    main()
