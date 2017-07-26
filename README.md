# My Website

The source code of my website, the aptly named [maxtimkovich.com](http://maxtimkovich.com).

## Projects
- [HearthSounds][1] - Get sound files of Hearthstone cards 
- [Top Tracks][2] - Show the most popular tracks for SoundCloud artists
- [Saved Posts][3] - Organize your saved reddit posts

## Usage

```bash
git submodule update --init --recursive
./make_requirements.txt.sh
python3 -m virtualenv venv
pip install -r requirements.txt
```

Run `run.sh` to start the Flask server. Will need to create a `flask_conf.sh`
in the parent directory for any configuration options.

## Author

Max Timkovich

## Licence

See the LICENSE file for more info.

[1]: https://github.com/mtimkovich/hearthsounds
[2]: https://github.com/mtimkovich/top_tracks
[3]: https://github.com/mtimkovich/saved_posts
