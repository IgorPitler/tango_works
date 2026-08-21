# Tongda TD-5000 console controls
#v1.0

import tongda_lib

def main():
    main_ip = "192.168.188.10"
    main_port = 502
    detector_ip = "192.168.188.30"
    detector_port = 502

    td_dev=tongda_lib.td5000(main_ip,main_port,detector_ip,detector_port)

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
                            td_dev.connect_all()
                            #print("connect all OK")
                        case "main":
                            td_dev.connect_main()
                            #print("connect main OK")
                        case "detector":
                            td_dev.connect_detector()
                            #print("connect detector OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "disconnect":
                try:
                    match command_input[1]:
                        case "all":
                            td_dev.disconnect_all()
                            #print("disconnect all OK")
                        case "main":
                            td_dev.disconnect_main()
                            #print("disconnect main OK")
                        case "detector":
                            td_dev.disconnect_detector()
                            #print("disconnect detector OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            # detector position
            case "position":
                try:
                    match command_input[1]:
                        case "home":
                            td_dev.command_detector_home()
                            #print("detector home sent")
                        case "stop":
                            td_dev.command_detector_stop()
                            #print("detector stop sent")
                        case "speed":
                            position = float(command_input[2])
                            td_dev.command_detector_speed(position)
                            #print("detector speed sent")
                        case "abs":
                            position = float(command_input[2])
                            #print(position)
                            if position < 85:
                                td_dev.command_detector_abs(position)
                                #print("detector abs OK")
                            else:
                                print("danger detector position! no action!")

                        case "rel":
                            position = float(command_input[2])
                            #print(position)
                            #print("detector rel OK")
                            td_dev.command_detector_rel(position)
                            # add DANGER position check later!!!
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "2theta":
                try:
                    match command_input[1]:
                        case "home":
                            td_dev.command_tetta_home()
                            #print("2theta home sent")
                        case "stop":
                            td_dev.command_tetta_stop()
                            #print("2theta stop sent")
                        case "speed":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_tetta_speed(position)
                            #print("2theta speed OK")
                        case "abs":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_tetta_abs(position)
                            #print("2theta abs OK")
                        case "rel":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_tetta_rel(position)
                            #print("2theta rel OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "omega":
                try:
                    match command_input[1]:
                        case "home":
                            td_dev.command_omega_home()
                            #print("omega home OK")
                        case "stop":
                            #print("omega stop OK")
                            td_dev.command_omega_stop()
                        case "speed":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_omega_speed(position)
                            #print("omega speed OK")
                        case "abs":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_omega_abs(position)
                            #print("omega abs OK")
                        case "rel":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_omega_rel(position)
                            #print("omega rel OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "kappa":
                try:
                    match command_input[1]:
                        case "home":
                            td_dev.command_kappa_home()
                            #print("kappa home OK")
                        case "stop":
                            td_dev.command_kappa_stop()
                            #print("kappa stop OK")
                        case "speed":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_kappa_speed(position)
                            #print("kappa speed OK")
                        case "abs":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_kappa_abs(position)
                            #print("kappa abs OK")
                        case "rel":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_kappa_rel(position)
                            #print("kappa rel OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            # ROTATE command is only on this axis!
            case "phi":
                try:
                    match command_input[1]:
                        case "home":
                            td_dev.command_phi_home()
                            #print("phi home OK")
                        # only on PHI axis!!!
                        case "rotate":
                            td_dev.command_phi_rotate()
                            #print("phi rotate OK")
                        case "stop":
                            td_dev.command_phi_stop()
                            #print("phi stop OK")
                        case "speed":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_phi_speed(position)
                            #print("phi speed OK")
                        case "abs":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_phi_abs(position)
                            #print("phi abs OK")
                        case "rel":
                            position = float(command_input[2])
                            #print(position)
                            td_dev.command_phi_rel(position)
                            #print("phi rel OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            # home all
            case "home":
                try:
                    match command_input[1]:
                        case "axis":
                            #detector first
                            #td_dev.command_detector_home()
                            td_dev.command_tetta_home()
                            td_dev.command_phi_home()
                            td_dev.command_omega_home()
                            td_dev.command_kappa_home()
                            #print("home all OK")

                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "shutter":
                try:
                    match command_input[1]:
                        case "open":
                            td_dev.command_shutter_open()
                            #print("shutter open OK")
                        case "close":
                            td_dev.command_shutter_close()
                            #print("shutter close OK")
                        case _:
                            print("command error")
                except Exception as e:
                    print("Wrong command.")

            case "limit":
                try:
                    match command_input[1]:
                        case "reset":
                            td_dev.command_limit_reset()
                            #print("limit reset OK")
                        case _:
                            print("command error")

                except Exception as e:
                    print("Wrong command.")

            case "status":
                td_dev.status()

            # TEST if it possible
            # phi
            case "move_all_abs":
                try:
                    phi_pos=float(command_input[1])
                    theta_pos=float(command_input[2])
                    omega_pos=float(command_input[3])
                    kappa_pos=float(command_input[4])
                    detector_pos=float(command_input[5])
                    td_dev.command_phi_abs(phi_pos)
                    td_dev.command_tetta_abs(theta_pos)
                    td_dev.command_omega_abs(omega_pos)
                    td_dev.command_kappa_abs(kappa_pos)
                    td_dev.command_detector_abs(detector_pos)

                except Exception as e:
                    print("Wrong command")

            case _:
                print("command error")


if __name__ == '__main__':
    main()