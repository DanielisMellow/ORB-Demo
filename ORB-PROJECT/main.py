import wifimgr
from time import sleep
import machine
import usocket as socket
from my_time import MyTime
from orb import LEDOrb
from fsm import SimpleFSM
from ir_tx.nec import NEC


wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass


def categorize_time(cur_time):
    if len(cur_time) < 3:
        return "other_time"
    hh, mm, ss = cur_time[0], cur_time[1], cur_time[2]

    if hh == 7 and mm == 1:
        return "on_trigger_time"
    elif hh == 23 and mm == 1:
        return "off_trigger_time"
    elif (hh >= 7) and (hh < 23):
        return "on_time"
    else:
        return "other_time"


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 80))
    s.listen(5)
except OSError as e:
    machine.reset()


def setup():
    global led
    global gate_pin
    global ir_tx
    global orb
    global light_fsm
    global now

    led = machine.Pin(2, machine.Pin.OUT)
    ir_tx = NEC(machine.Pin(19, machine.Pin.OUT, value=0))
    gate_pin = machine.Pin(4, machine.Pin.OUT, value=0)
    orb = LEDOrb(ir_tx, gate_pin)
    light_fsm = SimpleFSM(orb)
    now = MyTime()

    event = categorize_time(now.get_time())
    print(f"Current State:{light_fsm.current_state}")
    light_fsm.transition(event)


def loop():

    while True:
        cur_time = now.get_time()
        print(f"Current State:{light_fsm.current_state}")
        print(cur_time)
        event = categorize_time(cur_time)
        light_fsm.transition(event)
        sleep(5)


if __name__ == "__main__":
    setup()
    loop()
