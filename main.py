from converse.speak import speak
from converse.use_ai import use_ai
from modules.play_music import play


while True:
    print("Listening.....")
    query = speak()
    print(f"User: {query}")
    if "play" in query:
        play(query)

    elif query.lower() != "stop":
        use_ai(query)
    else:
        break