import os
import subprocess

if subprocess.call(
        ['which', 'gpg2'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) == 0:
    GPG_BIN = 'gpg2'
elif subprocess.call(
        ['which', 'gpg'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) == 0:
    GPG_BIN = 'gpg'
else:
    raise Exception("Could not find GPG")

class PasswordStore:
    def __init__(
            self,
            path=os.path.join(os.getenv("HOME"), ".password-store"),
            git_dir=None,
    ):
        self.password_store_path = os.path.abspath(path)
        self.gpg_id = self._get_gpg_id(self.password_store_path)

        git_dir = git_dir or os.path.join(self.password_store_path, '.git')
        self.uses_git = os.path.isdir(git_dir)
        if self.uses_git:
            self.git_dir = git_dir

    def _get_gpg_id(self, file_path):
        gpg_id_path = os.path.join(file_path, '.gpg-id')
        if os.path.isfile(gpg_id_path):
            with open(gpg_id_path, 'r') as gpg_id_file:
                return gpg_id_file.read().strip()
        raise Exception("could not find .gpg-id file")

    def get_passwords_list(self):
        passwords = []
        for root, dirnames, filenames in os.walk(self.password_store_path):
            for filename in filenames:
                if filename.endswith('.gpg'):
                    path = os.path.join(root, filename.replace('.gpg', ''))
                    simplified_path = path.replace(self.password_store_path + '/', '')
                    passwords.append(simplified_path)
        return passwords

    def get_decrypted_password(self, path):
        passfile_path = os.path.realpath(
            os.path.join(
                self.password_store_path,
                path + '.gpg'
            )
        )
        gpg = subprocess.Popen(
            [
                GPG_BIN,
                '--quiet',
                '--batch',
                '--use-agent',
                '-d', passfile_path,
            ],
            shell=False,
            stdout=subprocess.PIPE
        )
        gpg.wait()

        if gpg.returncode == 0:
            return gpg.stdout.read().decode()
        else:
            raise Exception("Couldn't decrypt {}".format(path))