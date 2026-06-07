#!/usr/bin/env python3
"""Run OpenCode CLI in non-interactive `opencode run` mode."""

import argparse
import os
import shlex
import shutil
import subprocess
import sys


def build_command(args):
    command = ["opencode", "run"]

    if args.command:
        command.extend(["--command", args.command])
    if args.attach:
        command.extend(["--attach", args.attach])
    if args.format:
        command.extend(["--format", args.format])
    if args.dir:
        command.extend(["--dir", args.dir])
    for file_path in args.file:
        command.extend(["--file", file_path])
    if args.model:
        command.extend(["--model", args.model])
    if args.agent:
        command.extend(["--agent", args.agent])
    if args.session:
        command.extend(["--session", args.session])
    if args.continue_last:
        command.append("--continue")
    if args.fork:
        command.append("--fork")
    if args.title:
        command.extend(["--title", args.title])
    if args.variant:
        command.extend(["--variant", args.variant])
    if args.thinking:
        command.append("--thinking")
    if args.port:
        command.extend(["--port", str(args.port)])
    if args.username:
        command.extend(["--username", args.username])

    command.append(" ".join(args.prompt))
    return command


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build and execute an `opencode run` command."
    )
    parser.add_argument("prompt", nargs="+", help="Prompt/message passed to OpenCode")
    parser.add_argument("--command", help="OpenCode command to run with the prompt as arguments")
    parser.add_argument("--attach", help="OpenCode server URL, for example $OPENCODE_SERVER_URL")
    parser.add_argument("--format", choices=["default", "json"], default="json", help="Output format")
    parser.add_argument("--dir", help="Project directory passed to OpenCode")
    parser.add_argument("--file", action="append", default=[], help="File to attach; repeat as needed")
    parser.add_argument("--model", help="Model in provider/model format")
    parser.add_argument("--agent", help="OpenCode agent name")
    parser.add_argument("--session", help="Session ID to continue")
    parser.add_argument("--continue-last", action="store_true", help="Continue the last OpenCode session")
    parser.add_argument("--fork", action="store_true", help="Fork the continued session")
    parser.add_argument("--title", help="Session title")
    parser.add_argument("--variant", help="Model variant")
    parser.add_argument("--thinking", action="store_true", help="Show OpenCode thinking blocks")
    parser.add_argument("--port", type=int, help="Local server port used by OpenCode run")
    parser.add_argument("--username", help="Basic Auth username for an attached server")
    parser.add_argument(
        "--password-env",
        help="Name of an environment variable whose value is forwarded as OPENCODE_SERVER_PASSWORD",
    )
    parser.add_argument("--local-cwd", help="Local cwd for launching the opencode process")
    parser.add_argument("--timeout", type=int, default=0, help="Timeout in seconds; 0 means no timeout")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running it")
    args = parser.parse_args()

    if args.continue_last and args.session:
        parser.error("--continue-last and --session cannot be used together")
    if args.fork and not (args.continue_last or args.session):
        parser.error("--fork requires --continue-last or --session")
    return args


def main():
    args = parse_args()
    command = build_command(args)
    rendered_command = " ".join(shlex.quote(part) for part in command)

    if args.dry_run:
        print(rendered_command)
        return 0

    if shutil.which("opencode") is None:
        print("error: opencode executable not found in PATH", file=sys.stderr)
        return 127

    env = os.environ.copy()
    if args.password_env:
        password = env.get(args.password_env)
        if not password:
            print("error: password environment variable is not set: {}".format(args.password_env), file=sys.stderr)
            return 2
        env["OPENCODE_SERVER_PASSWORD"] = password

    try:
        completed = subprocess.run(
            command,
            cwd=args.local_cwd or None,
            env=env,
            timeout=args.timeout if args.timeout > 0 else None,
        )
        return completed.returncode
    except subprocess.TimeoutExpired:
        print("error: opencode command timed out after {} seconds".format(args.timeout), file=sys.stderr)
        return 124
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
