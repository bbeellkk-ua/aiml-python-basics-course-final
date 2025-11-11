from assistant import Assistant

def main():
    with Assistant() as assistant:
        assistant.run()

if __name__ == "__main__":
    main()
