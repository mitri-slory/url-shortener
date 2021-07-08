from urlshort import create_app

#Test to check if the word Shorten is on the home page
def test_shorten(client):
    response = client.get('/')
    assert b'Shorten' in response.data