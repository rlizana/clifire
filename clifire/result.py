from clifire import out


class Result:
    def __init__(self, code: int = 0, stdout: str = "", stderr: str = ""):
        self.code = code
        self.stdout = self._clean_str(stdout)
        self.stderr = self._clean_str(stderr)
        out.debug2(f"Result: {self}")

    def _clean_str(self, value):
        value = value.decode("utf8") if isinstance(value, bytes) else value
        if value and value.endswith("\n"):
            value = value[:-1]
        return value

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
