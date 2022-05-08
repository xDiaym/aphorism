from pathlib import Path
import pytest


@pytest.fixture()
def audio_file() -> Path:
    return Path(__file__).parent / "example_sound.mp3"
