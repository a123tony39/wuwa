def add(a, b):
    return a + b

def test_add_numbers():
    assert add(2, 3) == 5

def test_add_strings():
    assert add("hello", "world") == "helloworld"