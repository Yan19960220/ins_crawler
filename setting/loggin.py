from instagrapi import Client

from utils.file import read_json

confid_file_path = '../setting/config.json'
ACCOUNT_USERNAME = read_json(confid_file_path, 'user_name')
ACCOUNT_PASSWORD = read_json(confid_file_path, 'password')

class Login:
    def __init__(self, user_name: str = ACCOUNT_USERNAME, passwd: str = ACCOUNT_PASSWORD):
        self.user_name = user_name
        self.passwd = passwd
        self.cl = Client()

    def login(self):
        print(f'Login in'.center(80, '*'))
        self.cl.login(self.user_name, self.passwd)

    def log_out(self):
        print(f'Login out'.center(80, '*'))
        self.cl.logout()
