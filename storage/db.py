from storage import encryption
import sqlite3
from os import getlogin, path, mkdir, getcwd, remove
from storage.exceptions import KeyDataDoesntFit, KeyFileNotFound
username = getlogin()
# directory of the db
# when config added, should be there
db_dir = f'C:\\Users\\{username}\\AppData\\Roaming\\Password Keeper\\pws.pws'
db_folder = f'C:\\Users\\{username}\\AppData\\Roaming\\Password Keeper'


def delete_db() -> None:
    if not path.exists(db_dir):
        raise FileNotFoundError
    remove(db_dir)


class DB:
    def __init__(self):
        self.conn = None
        self.c = None

        key_file = True
        if not encryption.k_data_exist():
            key_file = False
        if not path.exists(db_folder):
            mkdir(db_folder)

        if not path.exists(db_dir):
            if not key_file:
                # no key file and n db -> no problem
                encryption.create_k_data_file()
        else:
            if not key_file:
                # db, no key file -> can't decrypt the db
                raise KeyFileNotFound("Encryption key is missing")

        key, nonce = encryption.get_k_data_from_disk()
        self.encryptor = encryption.EncInterface(key, nonce)

    def connect(self):
        self.conn = sqlite3.connect(db_dir)
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS data(source TEXT, info TEXT, login BLOB, password BLOB)')

    def _get_enc_data(self) -> list:
        self.c.execute('SELECT * FROM data')
        return self.c.fetchall()

    def _decrypt(self, to_dec: bytes) -> str:
        return self.encryptor.decrypt(to_dec)

    def _decrypt_pws(self, password_data: list) -> list:
        result = []
        for source, info, login, password in password_data:
            decrypted_login = self._decrypt(login)
            decrypted_password = self._decrypt(password)
            result.append((source, info, decrypted_login, decrypted_password))
        return result

    def add_password(self, source, info, login, password):
        encrypted_login = self.encryptor.encrypt(login)
        encrypted_password = self.encryptor.encrypt(password)
        self.c.execute('INSERT INTO data(source, info, login, password) VALUES(?, ?, ?, ?)',
                       (source, info, encrypted_login, encrypted_password))
        # if there is another password with the same data, delete it
        self.c.execute('DELETE FROM data WHERE '
                       'source IN (SELECT source FROM data GROUP BY source HAVING count(*)>1) AND '
                       'info IN (SELECT info FROM data GROUP BY info HAVING count(*)>1) AND '
                       'login IN (SELECT login FROM data GROUP BY login HAVING count(*)>1) AND '
                       'password IN (SELECT password FROM data GROUP BY password HAVING count(*)>1)')
        self.conn.commit()

    def edit_password(self, old_data: tuple, new_data: tuple):
        old_data = (old_data[0], old_data[1], self.encryptor.encrypt(old_data[2]), self.encryptor.encrypt(old_data[3]))
        new_data = (new_data[0], new_data[1], self.encryptor.encrypt(new_data[2]), self.encryptor.encrypt(new_data[3]))
        self.c.execute("UPDATE data SET source = ?, info = ?, login = ?, password = ? WHERE "
                       "source = ? AND info = ? AND login = ? AND password = ?", new_data+old_data)
        self.conn.commit()

    def delete_password(self, source: str, info: str, login: str, password: str):
        login, password = self.encryptor.encrypt(login), self.encryptor.encrypt(password)
        self.c.execute('DELETE FROM data WHERE source=? AND info = ? AND login = ? AND password = ?',
                       (source, info, login, password,))
        self.conn.commit()

    def _get_pws(self, *, source: str, login: str, password: str):
        # the search takes places when a user is typing, so we need to search for alike password data
        # that's why % is added in the end if every field
        password = self.encryptor.encrypt(password) + b'%'
        source, login = source + '%', self.encryptor.encrypt(login) + b'%'
        self.c.execute('SELECT * FROM  data WHERE source LIKE ? AND login LIKE ? AND password LIKE ?',
                       (source, login, password))
        try:
            # can't decrypt, then k-data is wrong
            passwords = self._decrypt_pws(self.c.fetchall())
        except UnicodeDecodeError:
            raise KeyDataDoesntFit("Encryption key is not for this password database")
        return passwords

    def get_matched_passwords(self, *, source: str = '', login: str = '', password: str = '') -> list:
        if any((source, login, password)):
            return self._get_pws(source=source, login=login, password=password)
        raise ValueError('No password info given')
