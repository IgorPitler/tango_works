# Tongda TD-5000 console controls
#v1.0

def check_limits(phi, theta, omega, kappa, detector_pos):
    allow = True
    # here we will check if the axis positions are dangerous

    return allow


def main():
    main_ip = "192.168.188.10"
    main_port = 502
    detector_ip = "192.168.188.30"
    detector_port = 502
    main_connected=False
    detector_connected=False
    working = True

    print("Tongda TD-5000 console controls")

    while working:
        command_input=input("> ").strip().split()

        match command_input[0]:

            case "exit":
                working=False
                print("Exiting. See you later!")

            case "connect":
                try:
                    match command_input[1]:
                        case "all":
                            print("connect all OK")
                        case "main":
                            print("connect main OK")
                        case "detector":
                            print("connect detector OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "disconnect":
                try:
                    match command_input[1]:
                        case "all":
                            print("disconnect all OK")
                        case "main":
                            print("disconnect main OK")
                        case "detector":
                            print("disconnect detector OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "detector":
                try:
                    match command_input[1]:
                        case "home":
                            print("detector home OK")
                        case "stop":
                            print("detector stop OK")
                        case "speed":
                            position = float(command_input[2])
                            print(position)
                            print("detector speed OK")
                        case "abs":
                            position = float(command_input[2])
                            print(position)
                            if position < 85:
                                print("detector abs OK")
                            else:
                                print("danger detector position!")

                        case "rel":
                            position = float(command_input[2])
                            print(position)
                            print("detector rel OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "2theta":
                try:
                    match command_input[1]:
                        case "home":
                            print("2theta home OK")
                        case "stop":
                            print("2theta stop OK")
                        case "speed":
                            position = float(command_input[2])
                            print(position)
                            print("2theta speed OK")
                        case "abs":
                            position = float(command_input[2])
                            print(position)
                            print("2theta abs OK")
                        case "rel":
                            position = float(command_input[2])
                            print(position)
                            print("2theta rel OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "omega":
                try:
                    match command_input[1]:
                        case "home":
                            print("omega home OK")
                        case "stop":
                            print("omega stop OK")
                        case "speed":
                            position = float(command_input[2])
                            print(position)
                            print("omega speed OK")
                        case "abs":
                            position = float(command_input[2])
                            print(position)
                            print("omega abs OK")
                        case"rel":
                            position = float(command_input[2])
                            print(position)
                            print("omega rel OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "kappa":
                try:
                    match command_input[1]:
                        case "home":
                            print("kappa home OK")
                        case "stop":
                            print("kappa stop OK")
                        case "speed":
                            position = float(command_input[2])
                            print(position)
                            print("kappa speed OK")
                        case "abs":
                            position = float(command_input[2])
                            print(position)
                            print("kappa abs OK")
                        case "rel":
                            position = float(command_input[2])
                            print(position)
                            print("kappa rel OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            # ROTATE command is only on this axis!
            case "phi":
                try:
                    match command_input[1]:
                        case "home":
                            print("phi home OK")
                        # only on PHI axis!!!
                        case "rotate":
                            print("phi rotate OK")
                        case "stop":
                            print("phi stop OK")
                        case "speed":
                            position = float(command_input[2])
                            print(position)
                            print("phi speed OK")
                        case "abs":
                            position = float(command_input[2])
                            print(position)
                            print("phi abs OK")
                        case "rel":
                            position = float(command_input[2])
                            print(position)
                            print("phi rel OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            # home all
            case "home":
                try:
                    match command_input[1]:
                        case "all":
                            print("home all OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "shutter":
                try:
                    match command_input[1]:
                        case "open":
                            print("shutter open OK")
                        case "close":
                            print("shutter close OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "limit":
                try:
                    match command_input[1]:
                        case "reset":
                            print("limit reset OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "status":
                try:
                    print("status OK")
                except Exception as e:
                    pass

            case _:
                print("command error")


if __name__ == '__main__':
    main()