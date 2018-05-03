#!C:/Users/murga/AppData/Local/Programs/Python/Python36-32/python.exe
import json
if __name__ == "__main__":
    r = [
        {
         'name': 'Result Name From Python',
         'url': 'http://www.python.org',
         'snapshot': 'Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis...'
         },
         {
          'name': 'Google',
          'url': 'http://www.google.com',
          'snapshot': 'Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis...'
         },
         {
          'name': 'Yahoo',
          'url': 'http://www.yahoo.com',
          'snapshot': 'Snapshot of the website text. The search term should be in <b>BOLD</b> and trail off with elipsis...'
         }
    ]
    print(json.dumps(r))