from time import sleep
from typing import List, Dict, Union, Any

from vklancer import api as vk_api
from vklancer.utils import oauth as vk_auth

from util.link import Link
from util.logger import *
from util.optimize_folder_name import optimize_folder_name


class VK:
    # Using to ensure the greatest photo size as it can be for a given photo
    Photo_priorities: List[str] = [
        "photo_2560",
        "photo_1280",
        "photo_807",
        "photo_604",
        "photo_130",
        "photo_75"
    ]

    def __init__(
            self,
            app_id: int,
            scope: int,
            login: str,
            password: str,
            delay: float = 1.0):

        self.app_id = app_id
        self.scope = scope
        self.login = login
        self.password = password
        self.delay = delay

        self.__access_token = None
        self.__api = None

        self.__auth()

    def __auth(self):
        self.__access_token = vk_auth(
            login=self.login,
            password=self.password,
            app_id=self.app_id,
            scope=self.scope)

        self.__api = vk_api.API(
            token=self.__access_token,
            version='5.63')

    def get_links(
            self,
            lovers: List[Dict[str, Union[str, List[str]]]]) -> List[Link]:
        """
        Gathers all possible links from every lover
        :param lovers: List of all lovers with the info about them
        :return: List of Links
        """

        log('Gathering links from VK:', INFO)

        links: List[Link] = list()

        for lover in lovers:
            count: int = 0
            name: str = lover["last_name"] + ' ' + lover["first_name"]

            for account_id in lover['vk']:
                result: List[Link] = self.get_links_from_id(int(account_id), name)
                links.extend(result)
                count += len(result)

            log('\t{0}: {1}'.format(name, count), INFO)

        log('All links gathered', INFO)

        return links

    def get_links_from_id(
            self,
            account_id: int,
            name: str) -> List[Link]:
        """
        Gathers all possible links from the lover
        :param account_id: One of lover's VK ID
        :param name: Name of lover
        :return: List of Links from given VK ID
        """

        links: List[Link] = list()

        albums: Dict[int, str] = self.get_albums(owner_id=account_id)

        for album_id in albums.keys():
            links.extend(self.get_links_from_album(owner_id=account_id,
                                                   album_id=album_id,
                                                   album_title=albums[album_id],
                                                   name=name))

        return links

    def get_albums(
            self,
            owner_id: int) -> Dict[int, str]:
        """
        Gathers all the albums of given owner_id 
        :param owner_id: VK ID
        :return: Dictionary containing album_id's and their titles
        """

        sleep(self.delay)
        response: Dict[str, Any] = self.__api.photos.getAlbums(owner_id=owner_id,
                                                               need_system=1)
        result: Dict[int, str] = dict()

        if 'error' not in response.keys():
            for album in response["response"]["items"]:
                result[album["id"]] = album["title"]

        return result

    def get_links_from_album(
            self,
            owner_id: id,
            album_id: int,
            album_title: str,
            name: str) -> List[Link]:
        """
        Gathers all the Links from the album
        :param owner_id: VK ID
        :param album_id: Album ID
        :param album_title: Album title
        :param name: Lover's name
        :return: List of Links from given album
        """

        sleep(self.delay)
        response: Dict[str, Any] = self.__api.photos.get(owner_id=owner_id,
                                                         album_id=album_id,
                                                         need_system=1,
                                                         rev=1,
                                                         photo_sizes=0)

        result: List[Link] = list()

        if 'error' not in response.keys():
            for item in response['response']['items']:
                try:
                    url: str

                    for priority in VK.Photo_priorities:
                        if priority in item.keys():
                            url = item[priority]
                            break

                    path = '{0}/VK/{1}/'.format(name, optimize_folder_name(album_title))

                    result.append(Link(url=url, path=path, creation_time=int(item['date'])))
                except Exception as exception:
                    log('Unable to get link of photo with id={0} from album with album_id={1} by the '
                        'owner with owner_id={2}'.format(item["id"], album_id, owner_id), ERROR)
                    log(str(exception), ERROR)

        return result
