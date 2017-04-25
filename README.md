# LoverGet

LoverGet is a tool for downloading your lover's photo from `VK`

## Features
- It loads data from `JSON` - easy to edit 👌
- You can add as many lovers as you and your PC can - be abother one of VK's `backup servers` 🆘
- You can add as many IDs of your lovers as they've got - `Catch 'em all` 💥
- Saves photos with the name, which contains a date of its creation, and changes "Last change date" file property - store then in a `chronological order` ⌚

## Tech
* [Python 3](http://python.org)
* [VKLancer](https://github.com/pyvim/vklancer)

## Usage
### Required arguments
- `-j` | `--loverPath` - A path to the JSON file with your lover's info
- `-s` | `--savePath` - A path where all downloaded photos will be stored
- `-l` | `--vkLogin` - Your VK login for authentication
- `-p` | `--vkPass` - Your VK password for authentication

```sh
python3 loverget.py -j "/home/user/lovers.json" -s "/home/user/lovers/" -l "vk_login" -p "vk_pass"
```

## Todos
#### Instagram support
---
## License
#### MIT
