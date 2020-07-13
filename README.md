# weechat-fzf

Switch buffer in WeeChat using fzf.

Currently requires WeeChat to be run inside tmux, as fzf is opened in a separate tmux pane.

## Installation

Requires fzf to be installed.

Copy the `fzf.py` script into `~/.weechat/python`.

Load the script in WeeChat: `/script load fzf.py`.

## Usage

Run `/fzf` in WeeChat.

Optionally bind a key to it, e.g.: `/key bind ctrl-G /fzf`.
