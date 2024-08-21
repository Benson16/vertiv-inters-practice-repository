import time

# Chorus lyrics of "Perfect Strangers"
chorus = [
    "Maybe we're perfect strangers",
    "Maybe it's not forever",
    "Maybe the night will change us",
    "Maybe we'll stay together",
    "Maybe we'll walk away",
    "Maybe we'll realize",
    "We're only human",
    "Maybe we don't need no reason"
]

# Function to display the lyrics letter by letter with a delay
def display_lyrics_per_letter(lyrics, delay=0.1):
    for line in lyrics:
        for letter in line:
            print(letter, end='', flush=True)
            time.sleep(delay)
        print()  # Move to the next line after each line is printed
        time.sleep(0.5)  # Slight delay between lines

# Display the chorus with each letter appearing one by one
display_lyrics_per_letter(chorus, delay=0.1)
