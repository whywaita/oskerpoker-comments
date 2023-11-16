# oskerpoker-comments

Generate timestamp comment in playing timing.

## Usage

Prepare by poetry.

```bash
$ poetry install --no-interaction
```

### parse-movie

`parse-movie` parse movie and generate timestamp comment.

```bash
$ poetry run python3 parse-movie main.py --file_path ./<file_path>.mp4
01:50:03 FOO vs BAR
01:51:11 BAZ vs BAX
01:53:42 BAX vs FOO
01:55:12 FOL vs BAZ
01:59:20 BAZ vs BAR
```

### get-playername

`get-playername` get player name from output of `parse-movie`.

```bash
$ $(command of parse-movie) | poetry run python3 main.py get-playe-rname
```

### autofix-playername

`autofix-playername` fix player name from output of `parse-movie`.

```bash
$ $(command of parse-movie) | poetry run python3 main.py autofix-player-name --correct-player-name '["FOO", "BAR", "BAZ"]'
01:50:03 FOO vs BAR
01:51:11 BAZ vs BAX
01:53:42 BAX vs FOO
01:55:12 FOL vs BAZ
01:59:20 BAZ vs BAR
```

## Restrictions

- Only support Heads up in post-flop.
- Only support 720p video.