import sys
from time import sleep
import time
import webbrowser

def lyrics():
    lines = [
        ("Well, I never saw it coming", 0.05),
        ("I should've started running,", 0.05),
        ("A long long time ago,", 0.10),
        ("And I never thought to doubt you,", 0.10),
        ("I'm better off without you,", 0.05),
        ("More than you, More than you know,", 0.08),
        ("I'm slowly getting closure,", 0.05, True),
        ("I guess it's really over,", 0.05),
        ("I'm finally getting better,", 0.13),
        ("And now I'm picking up the pieces and spending all of these years,", 0.05),
        ("Putting my heart back together cause", 0.04),
        ("The day I thought I'll never get through,", 0.09),
        ("I got over you,", 0.05),
    ]
    delays = [0.05, 0.05, 0.05, 0.10, 0.05, 0.08, 0.05, 0.05, 0.13, 0.05, 0.04, 0.09, 0.05]

    for i, (line, char_delay) in enumerate(lines):
        for char in line:  
            print(char, end='')
            sys.stdout.flush()
            sleep(char_delay)
        time.sleep(delays[i])
        print('')

webbrowser.open("https://www.youtube.com/watch?v=UIYC4m3kQwY&pp=ygUYb3ZlciB5b3UgZGF1Z2h0cnkgbHlyaWNz")

lyrics()
