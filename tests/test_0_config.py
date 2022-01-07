from typing import Any, Optional

import isisdl.bin.config as config
from isisdl.backend.utils import config_helper


def assert_config_expected(username: Optional[str], clean_pw: Optional[str], encrypted_pw: Optional[str], filename_scheme: str, throttle_rate: Optional[int], update_policy: str,
                           telemetry: str) -> None:
    items = {
        username: config_helper.get_user(),
        clean_pw: config_helper.get_clear_password(),
        encrypted_pw: config_helper.get_encrypted_password(),
        filename_scheme: config_helper.get_filename_scheme(),
        throttle_rate: config_helper.get_throttle_rate(),
        update_policy: config_helper.get_update_policy(),
        telemetry: config_helper.get_telemetry(),
    }

    for a, b in items.items():
        assert a == b


def test_config_default(monkeypatch: Any) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "0")

    config.main()

    assert_config_expected(None, None, None, "0", None, "0", "1")


def test_config_default_no_prompt(monkeypatch: Any) -> None:
    choices = iter(["", "2", "", "", "", "", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(choices))

    config.main()

    assert_config_expected(None, None, None, "0", None, "0", "1")


def test_config_input(monkeypatch: Any) -> None:
    choices = iter(["2", "2", "2", "1", "0", "55", "0", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(choices))

    config.main()

    assert_config_expected(None, None, None, "1", 55, "2", "2")