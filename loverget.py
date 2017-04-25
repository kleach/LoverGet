from argparse import ArgumentParser
from json import load as json_load
from typing import Dict, List, Union

from util.downloader import Downloader
from util.vk import VK

CONFIG_PATH = 'settings/config.json'


def main():
    arg_parser = ArgumentParser(prog='LoverGet',
                                description='A program for getting your lover\'s photos from social networks',
                                epilog='© 2015, Dmitry Petrushin')

    arg_parser.add_argument('-j', '--loverPath',
                            help='A path to the JSON file with your lover\'s info',
                            required=True,
                            dest='lover_path')
    arg_parser.add_argument('-s', '--savePath',
                            help='A path where all downloaded photos will be stored',
                            required=True,
                            dest='save_path')
    arg_parser.add_argument('-l', '--vkLogin',
                            help='Your VK login for authentication',
                            required=True,
                            dest='vk_login')
    arg_parser.add_argument('-p', '--vkPass',
                            help='Your VK password for authentication',
                            required=True,
                            dest='vk_password')

    args = arg_parser.parse_args()

    with open(CONFIG_PATH, 'r') as config_file:
        config: Dict[str, int] = json_load(config_file)
    with open(args.lover_path, 'r') as lover_path:
        lovers: List[Dict[str, Union[str, List[str]]]] = json_load(lover_path)['lovers']

    vk_links = VK(app_id=config['vk_app_id'],
                  scope=config['vk_scope'],
                  login=args.vk_login,
                  password=args.vk_password).get_links(lovers=lovers)

    not_downloaded = Downloader().download(links=vk_links, save_path=args.save_path)
    if len(not_downloaded) > 0:
        while len(not_downloaded) > 0:
            not_downloaded = Downloader.download(links=not_downloaded, save_path=args.save_path)


if __name__ == '__main__':
    main()
