import hashlib





def test():
    m = hashlib.sha256()
    m.update(b"hello world")
    r = m.digest().hex()
    assert r == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

test()