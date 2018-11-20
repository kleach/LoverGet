# PhotoGett

PhotoGett is a tool for downloading someone's photos from `VK`

## Features
- It loads data from `JSON` - easy to moderate needed people 👌
- You can add as many people as you and your PC can - be abother one of VK's `backup servers` 🆘
- You can add as many IDs of some person as he/she/_ got - `Catch 'em all` 💥
- It saves photos with the name, which contains a date of its creation, and changes "Last change date" file property - store them in a `chronological order` ⌚

## Tech
* [Python 3](http://python.org)
* [VKLancer](https://github.com/pyvim/vklancer)

## Usage
### Required arguments
- `-j` — A path to the JSON file with your lover's info
- `-s` — A path where all downloaded photos will be stored
- `-l` — Your VK login for authentication
- `-p` — Your VK password for authentication

```sh
python3 photogett.py -j "/home/user/people.json" -s "/home/user/people/" -l "vk_login" -p "vk_pass"
```

## Todos
- Instagram support
---
## License
#### MIT
