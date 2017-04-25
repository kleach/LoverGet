class Link:
    def __init__(
            self,
            url: str,
            path: str,
            creation_time: float):
        self.url: str = url
        self.path: str = path
        self.filename: str = self.get_filename(self.url)
        self.extension: str = self.get_extension(self.filename)
        self.creation_time: int = creation_time

    @staticmethod
    def get_filename(url: str) -> str:
        return url.split('/')[::-1][0]

    @staticmethod
    def get_extension(filename: str) -> str:
        return filename.split('.')[::-1][0]
