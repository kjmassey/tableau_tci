import requests
import json

def get_all_breeds():
    '''
    Dog API: Send a simple GET, returns a JSON object with all available breeds
    '''
    url = 'https://dog.ceo/api/breeds/list/all'

    resp = requests.get(url)

    return resp.content

def random_image_by_breed(breed_name):
    '''
    Dog API: Return random images of the specified breed
    '''
    
    # f strings are CRUCIAL, learn to love them!
    url = f"https://dog.ceo/api/breed/{breed_name}/images/random/3"

    resp = requests.get(url)

    # Sometimes you'll need resp.content, other times resp.text -
    # consult your API's documentation
    return json.loads(resp.content)


########
# SCRATCH AREA
########


# print(get_all_breeds())
print(random_image_by_breed('retriever'))
