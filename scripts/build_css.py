#!/usr/bin/env python3
"""Tailwind CSS build orchestrator stub.

This script will be expanded to invoke the pnpm Tailwind build pipeline once the
frontend tooling has been configured. For now it simply reports that the build
step is not yet implemented.
"""

import sys


def main() -> int:
    """Entry point."""
    print("Tailwind build pipeline is not configured yet.\n"
          "Set up the frontend tooling and update scripts/build_css.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
