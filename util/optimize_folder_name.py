from re import sub


def optimize_folder_name(folder_name: str) -> str:
    """
    Optimizes album name for using as folder name
    :param folder_name: A folder name to be optimized.
    :return: Optimized folder name, according to the Windows accepted symbols of folder name.
    """
    result: str = sub(r'[\\/:"<>?&*|]', '', folder_name).strip()
    if result == '':
        result = 'Forbidden folder name'

    return result
