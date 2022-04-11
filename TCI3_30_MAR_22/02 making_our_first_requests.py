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
    # https://realpython.com/python-f-strings/

    # url = "https://dog.ceo/api/breed/{}/images/random/3".format(breed_name)
    url = f"https://dog.ceo/api/breed/{breed_name}/images/random/3"

    resp = requests.get(url)

    # Sometimes you'll need resp.content, other times resp.text -
    # consult your API's documentation
    return json.loads(resp.content)


########
# SCRATCH AREA
########


# all_breeds = get_all_breeds()
# print('PRINTING ALL PRINTS AS: ', type(all_breeds))
# print(all_breeds)

random_img_by_breed = random_image_by_breed('retriever')

print('PRINTING RANDOM IMAGE RESTULS AS: ', type(random_img_by_breed))
print(random_img_by_breed)
