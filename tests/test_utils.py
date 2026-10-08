from app.utils import sha256
def test_sha256(): assert len(sha256(b'hello'))==64
