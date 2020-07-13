from typing import Iterator, Tuple
import weechat


SCRIPT_NAME = "fzf"
SCRIPT_AUTHOR = "Trygve Aaberge <trygveaa@gmail.com>"
SCRIPT_VERSION = "0.1.0"
SCRIPT_LICENSE = "MIT"
SCRIPT_DESC = "Switch buffer using fzf (currently only works inside tmux)"
REPO_URL = "https://github.com/trygveaa/weechat-fzf"


def print_error(message: str) -> None:
    weechat.prnt("", weechat.prefix("error") + message)


def fzf_process_cb(
    data: str, command: str, return_code: int, out: str, err: str
) -> int:
    if return_code == weechat.WEECHAT_HOOK_PROCESS_ERROR or return_code == 2 or err:
        print_error("Error running fzf (code {}): {}".format(return_code, err))
        return weechat.WEECHAT_RC_OK
    if out != "":
        pointer, number, name = out.split("\t")
        weechat.buffer_set(pointer, "display", "1")
    return weechat.WEECHAT_RC_OK


def fzf_command_cb(data: str, buffer: str, args: str) -> int:
    cmd = "fzf-tmux -- --delimiter='\t' --with-nth=2.."
    hook = weechat.hook_process_hashtable(cmd, {"stdin": "1"}, 0, "fzf_process_cb", "")
    for buffer_info in buffers():
        weechat.hook_set(hook, "stdin", "\t".join(buffer_info) + "\n")
    weechat.hook_set(hook, "stdin_close", "")
    return weechat.WEECHAT_RC_OK


def buffers() -> Iterator[Tuple[str, str, str]]:
    infolist = weechat.infolist_get("buffer", "", "")
    while weechat.infolist_next(infolist):
        pointer = weechat.infolist_pointer(infolist, "pointer")
        number = weechat.infolist_integer(infolist, "number")
        name = weechat.infolist_string(infolist, "name")
        yield (pointer, str(number), name)
    weechat.infolist_free(infolist)


def main() -> None:
    if not weechat.register(
        SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""
    ):
        return

    tmux = weechat.string_eval_expression("${env:TMUX}", {}, {}, {})
    if not tmux:
        print_error("Error: fzf.py currently only supports being run inside tmux")
        return

    weechat.hook_command(SCRIPT_NAME, SCRIPT_DESC, "", "", "", "fzf_command_cb", "")


if __name__ == "__main__":
    main()
