#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import argparse

from lib.utils.git import get_repo_info, load_beman_standard_config
from lib.pipeline import run_checks_pipeline


def parse_args():
    """
    Parse the CLI arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path", help="path to the repository to check", type=str)
    parser.add_argument(
        "--fix-inplace",
        help="Try to automatically fix found issues",
        action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--verbose",
        help="print verbose output for each check",
        action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
    )
    parser.add_argument(
        "--checks", help="array of checks to run", type=str, default=None
    )
    args = parser.parse_args()

    args.repo_info = get_repo_info(args.repo_path)
    args.checks = args.checks.split(",") if args.checks else None

    return args


def main():
    """
    The beman-tidy main entry point.
    """
    args = parse_args()

    beman_standard_check_config = load_beman_standard_config(".beman-standard.yml")
    if not beman_standard_check_config or len(beman_standard_check_config) == 0:
        print("Failed to download the beman standard. STOP.")
        return

    checks_to_run = (
        [check for check in beman_standard_check_config]
        if args.checks is None
        else args.checks
    )

    run_checks_pipeline(checks_to_run, args, beman_standard_check_config)


if __name__ == "__main__":
    main()
