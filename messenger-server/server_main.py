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



def main():
    #server_pub_key = Encryptor.load_private_key('test_public_key.pem')
    #server_pr_key = Encryptor.load_private_key('test_private_key.pem')
    #Users.deserialize()
    #server = Server('192.168.1.40', 65000)
    #server.run()
    #Users.serialize()
    # test_encryption_time()
    # test_hash_time()
    pass

if __name__ == "__main__":
    main()
