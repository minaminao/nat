import argparse
import sys
import openai
import os
import re
import tty
import termios
import colorama
from enum import Enum

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class Action(Enum):
    PREVIOUS = 1
    NEXT = 2
    SELECT = 3
    ABORT = 4


def read_actions():
    while True:
        match get_key():
            case "↑" | "k":
                yield Action.PREVIOUS
            case "↓" | "j":
                yield Action.NEXT
            case "\x03" | "q":
                yield Action.ABORT
            case "\n" | "\r":
                yield Action.SELECT


def select_command(commands):
    selected_command_id = 0
    print_commands(commands, selected_command_id, first=True)
    for action in read_actions():
        match action:
            case Action.SELECT:
                sys.stderr.write("\n")
                return selected_command_id
            case Action.ABORT:
                return None
            case Action.PREVIOUS:
                selected_command_id = (selected_command_id - 1 + len(commands)) % len(commands)
                print_commands(commands, selected_command_id)
            case Action.NEXT:
                selected_command_id = (selected_command_id + 1) % len(commands)
                print_commands(commands, selected_command_id)


def print_commands(commands, selected_command_id, first=False):
    if not first:
        for _ in range(len(commands)):
            sys.stderr.write("\033[1A\033[2K")
    for command_id, command in enumerate(commands):
        if command_id == selected_command_id:
            sys.stderr.write((u"(x) {bold}{command}{reset} ({green}Enter{reset}|{blue}↑{reset}|{blue}↓{reset})\n").format(command=command, bold=colorama.Style.BRIGHT, green=colorama.Fore.GREEN, reset=colorama.Style.RESET_ALL, blue=colorama.Fore.BLUE))
        else:
            sys.stderr.write((u"( ) {bold}{command}{reset}\n").format(command=command, bold=colorama.Style.BRIGHT, reset=colorama.Style.RESET_ALL))


def query(prompt):
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Output three terminal commands in list format that do the following and each output command must be enclosed in ###.\n {prompt}"}])
        return response
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="nat: a toy tool to execute commands using natural language powered by ChatGPT", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("prompt", nargs="*", help="A prompt for ChatGPT")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print the response from ChatGPT")

    args = parser.parse_args()

    if not args.prompt:
        print("Error: the prompt argument is required\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    prompt = " ".join(args.prompt)
    response = query(prompt)
    if args.verbose:
        print(response)
    content = response["choices"][0]["message"]["content"]
    commands = []
    for command in re.findall(r"###([^#]+)###", content):
        if command.startswith("\n"):
            command = command[1:]
        if command.endswith("\n"):
            command = command[:-1]
        commands.append(command)
    
    command_id = select_command(commands)
    if command_id is not None:
        os.system(commands[command_id])
