def test_hello_world(client, db):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == "Hello World"
