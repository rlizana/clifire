class Result:
    def __init__(self, code: int = 0, stdout: str = "", stderr: str = ""):
        self.code = code
        self.stdout_raw = (
            stdout.decode("utf8") if isinstance(stdout, bytes) else stdout
        )
        self.stderr_raw = (
            stderr.decode("utf8") if isinstance(stderr, bytes) else stderr
        )

    def _raw_to_list(self, txt: str) -> list:
        return txt.split("\n")

    @property
    def stdout(self) -> str:
        if self.stdout_raw:
            return self._raw_to_list(self.stdout_raw)
        return ""

    @property
    def stderr(self) -> str:
        if self.stderr_raw:
            return self._raw_to_list(self.stderr_raw)
        return ""

    def __bool__(self) -> bool:
        return self.code == 0

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(
            {
                "code": self.code,
                "stdout": self.stdout,
                "stderr": self.stderr,
            }
        )


class ResultOk(Result):
    def __init__(self, stdout: str = ""):
        super().__init__(code=0, stdout=stdout)


class ResultError(Result):
    def __init__(self, stderr: str = "", code: int = 1):
        super().__init__(code=code, stderr=stderr)
