from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "rock-groove-382223",
  "private_key_id": "0849791e08de098e579e14b8e4d744d3ae6414e1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0l31WPx2/x7jN\nCEG1W5hzIzdIrVZ5uhDEYqDm5AazeQM0rspDCWDFylEz3IX8xHwirwYgaAjJwSE6\nKUMPxE3oV4fpVVBc/RfM/yCBmxvpF1vRsHkg7k9rrCg0aIuU7q1zKPC80RiZrIBe\nA0/HdNORlp+5boKEZaRfcuqR+0BSTGO0ZnTMm7I5w130QJ5hap4QZvfLH0xMU4DQ\nTTDLF/PIjeZxmmKdQk/ROQjS8avfFa7VfPtZBqUDjjf1QU14mQWRLHpFhO1xdOOh\noZ7mgaDzB6aZ3lQlxrzDFQJX7JviQYV+x9l9t1rOA449U1iEjXw4yx9AwNhZ3aQh\nQZzPJNzNAgMBAAECggEAK0Kn3md3tad/FDSQYwSqWBh9R45oavgAyL6Uq0K//TG1\nrCLb5mOieDcPLTR8L1EVKIzTU6OASW5XipJ0U1xTyl7feqx6eBAT6cJK8+knbjav\nguN6nMIhqdofdnB90WM8jxvlUWHoefWZ+YtjCtVoUhWqNPYtU1By5/+EBAzTO3NU\neKyw1trR9pPlQki6f/LD+aToxVK+ZVfR3vuup6lhEzyTCsjHSkxwh/MU59R4Px0Y\ntxq8eg7IPMmYeJKui7ak5ZoDzmsahRkOdjv4xe7DJT/X0F4Nmal31gpvnlnUgDNr\n/u5mjgRObABvSJkXLl8nUxIrNW3KWV2qUAMpX5sFIQKBgQDjdFpPWSZsD+vLDOnR\nBsdkcGlVNlPn/NcANL8YZZE6EPUVVAoYFZJCBifBw2NsjJNOFp3wQ8lU4ya2WKl/\nxy1MzQNcxZhtXKlLj9nty/Pjw7pFTGSm9nZG8Uk4BAFLyHbsl7+VNN7vE+cHjoGb\nf5Y5p2S6TbzVTg5mmnqThVvXbQKBgQDLQYhjs0ulgmBjXPl1hS1NPkBc2tjXVMUs\nRP23Fwvq0XodhJMly1XqDRlPlyu4365v02oH0BNGKYOknnhF3ZePXCnG8yz3DN1w\nxjAvDokCQ1bN4VQfhcdJKwZhkOb9cUoQ7tpbIZ5G4J4VuBAklSm3oww9PcfyR84W\ne1GJmYze4QKBgQCaRPZjzxGSRZIl3BJSJYjjhKLMmtZ6CDFDAIOD5o+DlLDF0IQw\nJaFXipk4gG9U1luqoQhqR2+sVYySLLx53/vHlV1sdNCXjDt+9ohXEvfOSZhzHAdA\nfvVl1I1WotDGN6cBfUMBziROf2843tzlPLoFTJWzDrq+6fw2dxwgJllOWQKBgAiq\nUJA/kpgJyOYzjocOGHJUlxXeVqRHfuh2QILPvrhSGeysPEG+O3lw+YVFIp4NGzi1\nQK34lvnEx1H7V5FS8yUvfrB2qZIWwFIQgPlgm0K3cDnyw01cvLRH20vJi69+ZvP1\n2uVLt5258cNnR3jnyxGDKABsY9vWZ9jZhQ5it3jBAoGAImXdZY8GK5epyPSC8EV4\ndkJQtiOeAhZCjdM4xv9gtObotb5BgUIuwHYEESHcQB9ze4wocB4iYEooDbb+gE3D\nTPIHU2szvTRI4GGjeBcfwNPs7byFszsFw+FuA8s7ayTYW4uPkBeZRJ7aSNOo3acV\nHKtK9fLKjfEHII+ddrdM1a0=\n-----END PRIVATE KEY-----\n",
  "client_email": "myaccount@rock-groove-382223.iam.gserviceaccount.com",
  "client_id": "112948700956119049206",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myaccount%40rock-groove-382223.iam.gserviceaccount.com"
}


try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
