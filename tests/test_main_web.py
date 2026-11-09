from mainWeb import app

def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200 # code HTTP signifiant que la requête s'est bien déroulée
