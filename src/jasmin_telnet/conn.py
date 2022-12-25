import pexpect
from pexpect import spawn

from jasmin_telnet.exceptions import (TelnetConnectionTimeout,
                                      TelnetLoginFailed,
                                      TelnetUnexpectedResponse)


class TelnetConnection(object):
    def __init__(self, host: str = "127.0.0.1", port: int = 8990, timeout: int = 10, auth: bool = True, username: str = "jcliadmin", password: str = "jclipwd", standard_prompt: str = "jcli : ", interactive_prompt: str = "> "):
        self.STANDARD_PROMPT = standard_prompt
        self.INTERACTIVE_PROMPT = interactive_prompt
        try:
            telnet: spawn = pexpect.spawn(
                f"telnet {host} {port}", timeout=timeout)
            if auth:
                telnet.expect_exact("Username: ")
                telnet.sendline(username)
                telnet.expect_exact("Password: ")
                telnet.sendline(password)
        except pexpect.EOF:
            raise TelnetUnexpectedResponse
        except pexpect.TIMEOUT:
            raise TelnetConnectionTimeout
        try:
            telnet.expect_exact(self.STANDARD_PROMPT)
        except pexpect.EOF:
            raise TelnetLoginFailed
        else:
            self.telnet = telnet
            self.telnet.setwinsize(200, 4000)
            self.telnet.maxread = 4000

    def __del__(self):
        "Make sure telnet connection is closed when unleashing response back to client"
        try:
            self.telnet.sendline("quit")
        except pexpect.ExceptionPexpect:
            self.telnet.kill(9)
