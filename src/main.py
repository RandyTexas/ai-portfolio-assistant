from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from watchlist import WATCHLIST


def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"Mode: {DEFAULT_MODE}")
    print(f"Current watchlist ({len(WATCHLIST)} stocks):")
    for ticker in WATCHLIST:
        print(f"- {ticker}")


if __name__ == "__main__":
    main()