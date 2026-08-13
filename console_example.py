
def main():
    print("Console control demo")

    working=True
    while working:
        command_input=input("> ").strip().split()

        if command_input[0]=="exit":
            working=False
            print("See you later!")
        elif command_input[0]=="init":
            print("Initialising...")
        elif command_input[0]=="start":
            try:
                position=float(command_input[2])
                print("starting "+command_input[1]+" "+command_input[2])
                print(position*2)
            except Exception as e:
                print(e)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()