from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from watchlist import WATCHLIST


def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"Mode: {DEFAULT_MODE}")
    print(f"Current watchlist ({len(WATCHLIST)} stocks):")
    for item in WATCHLIST:
        print(f"- {item['ticker']} ({item['category']})")


if __name__ == "__main__":
    main()