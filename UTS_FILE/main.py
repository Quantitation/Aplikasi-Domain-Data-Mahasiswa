"""Titik masuk aplikasi.

  python main.py                      -> mode menu interaktif
  python main.py <perintah> <file>    -> mode perintah (lihat README)
"""
import sys

from akademik import cli, menu

if __name__ == "__main__":
    sys.exit(cli.main() if len(sys.argv) > 1 else menu.main())
