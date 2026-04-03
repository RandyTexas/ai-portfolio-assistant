from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from watchlist import WATCHLIST


def display_watchlist(watchlist):
    print(f"Current watchlist ({len(watchlist)} stocks):")
    for item in watchlist:
        print(f"- {item['ticker']} ({item['category']})")


def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"Mode: {DEFAULT_MODE}")
    display_watchlist(WATCHLIST)


if __name__ == "__main__":
    main()