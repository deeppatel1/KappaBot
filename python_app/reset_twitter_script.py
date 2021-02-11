import os, subprocess, time

while True:
    print('---in reset twitter script')
    try:
        subprocess.run(["python3","python_app/tweet_posts.py"], timeout=60 * 110)
    except subprocess.TimeoutExpired:
        print('---- in pass script, of except clause')
        pass
    time.sleep(25)