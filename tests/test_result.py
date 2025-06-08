from clifire import result


def test_result():
    res = result.Result(0, "OK", "KO")
    assert bool(res) is True
    assert res.code == 0
    assert str(res)
    assert str(res) == res.__repr__()

    res = result.ResultOk("OK")
    assert bool(res) is True
    assert res.code == 0
    assert res.stdout == "OK"
    assert res.stderr == ""

    res = result.ResultError("ERROR", 99)
    assert bool(res) is False
    assert res.code == 99
    assert res.stdout == ""
    assert res.stderr == "ERROR"
