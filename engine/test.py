import json
if __name__ == "__main__":
    r = {
        "1": {
            "name": "Result Name From Python",
            "url": "http://www.python.org",
            "snapshot": "Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis..."
        },
        "2": {
            "name": "Google",
            "url": "http://www.google.com",
            "snapshot": "Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis..."
        },
        "3": {
            "name": "Yahoo",
            "url": "http://www.yahoo.com",
            "snapshot": "Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis..."
        }
    }
    print(json.dumps(r, sort_keys=True))
