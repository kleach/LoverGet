from os import makedirs
from os import path as ospath
from os import utime as modify_change_time
from pickle import dump as save_existing_file_names, load as load_existing_file_names
from time import gmtime as get_time, strftime
from typing import List, Set
from urllib import request

from util.link import Link
from util.logger import *


class Downloader:
    @staticmethod
    def download(links: List[Link], save_path: str) -> List[Link]:
        """
        Downloads all the links according to their 'path' parameter
        :param links: List of Links to be downloaded
        :param save_path: Path to directory where downloaded photos will be saved
        :return: List of Links which had not been downloaded
        """
        downloaded_count: int = 0
        existing_count: int = 0
        trouble_photos: List[Link] = list()

        log('Downloading images:', INFO)

        for link in links:
            path = save_path + link.path

            # Using a set containing origin names of photos to prevent multiple-time downloading
            try:
                with open(path + 'files.txt', 'rb') as file:
                    existing: Set[str] = load_existing_file_names(file)
            except (OSError, IOError):
                if not ospath.exists(path):
                    makedirs(path)
                with open(path + 'files.txt', 'wb+') as file:
                    existing: Set[str] = set()
                    save_existing_file_names(existing, file)

            try:
                if link.filename not in existing:
                    filename: str = 'IMG_{0}.{1}'.format(strftime('%Y_%m_%H-%M-%S', get_time(link.creation_time)),
                                                         link.extension)
                    with open(path + filename, 'wb') as img:
                        img.write(request.urlopen(link.url).read())
                    modify_change_time(path + filename, (link.creation_time, link.creation_time))

                    downloaded_count += 1
                    existing.add(link.filename)
                    log('\t' + filename, INFO)
                else:
                    existing_count += 1
            except Exception as exception:
                trouble_photos.append(link)
                log('\tException occurred.\n\t{0}'.format(exception), ERROR)
            finally:
                with open(path + 'files.txt', 'wb') as file:
                    save_existing_file_names(existing, file)

        log('{0} photos has been downloaded'.format(downloaded_count), INFO)
        if downloaded_count + existing_count != len(links):
            log('{0} photos has not been downloaded'.format(len(links) - downloaded_count - existing_count), ERROR)
        else:
            log('DONE', INFO)

        return trouble_photos
