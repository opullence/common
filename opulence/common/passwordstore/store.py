import os
import subprocess

from opulence.common.patterns import Singleton

if (
    subprocess.call(["which", "gpg2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    == 0
):
    GPG_BIN = "gpg2"
elif (
    subprocess.call(["which", "gpg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    == 0
):
    GPG_BIN = "gpg"
else:
    raise Exception("Could not find GPG")


class Store(Singleton):
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.getenv("HOME"), ".password-store")
        self.password_store_path = os.path.abspath(path)

    def get_passwords_list(self):
        passwords = []
        for root, _, filenames in os.walk(self.password_store_path):
            for filename in filenames:
                if filename.endswith(".gpg"):
                    path = os.path.join(root, filename.replace(".gpg", ""))
                    simplified_path = path.replace(self.password_store_path + "/", "")
                    passwords.append(simplified_path)
        return passwords

    def get_decrypted_password(self, path):
        passfile_path = os.path.realpath(
            os.path.join(self.password_store_path, path + ".gpg")
        )
        gpg = subprocess.Popen(
            [GPG_BIN, "--quiet", "--batch", "--use-agent", "-d", passfile_path],
            shell=False,
            stdout=subprocess.PIPE,
        )
        gpg.wait()

        if gpg.returncode == 0:
            res = gpg.stdout.read().decode()
            return res[:-1]
        else:
            return None
