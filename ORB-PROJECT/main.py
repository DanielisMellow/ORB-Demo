import wifimgr
from time import sleep
from machine import Pin, Timer, reset
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

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 80))
    s.listen(5)
except OSError as e:
    reset()


## FSM Driver
def categorize_time(cur_time):
    if len(cur_time) < 3:
        return "other_time"
    hh, mm, _ = cur_time[0], cur_time[1], cur_time[2]

    if hh == 7 and mm == 1:
        return "on_trigger_time"
    elif hh == 23 and mm == 1:
        return "off_trigger_time"
    elif (hh >= 7) and (hh < 23):
        return "on_time"
    else:
        return "other_time"


# Callback function for the timer
def timer_callback(timer):
    cur_time = now.get_time()
    print(f"Time:{cur_time}")
    event = categorize_time(cur_time)
    print(f"Event:{event}")
    light_fsm.transition(event)


def setup():
    global led
    global gate_pin
    global ir_tx
    global orb
    global light_fsm
    global now
    global event_timer

    led = Pin(2, Pin.OUT)
    ir_tx = NEC(Pin(19, Pin.OUT, value=0))
    gate_pin = Pin(4, Pin.OUT, value=0)
    orb = LEDOrb(ir_tx, gate_pin)
    light_fsm = SimpleFSM(orb)
    now = MyTime()
    event = categorize_time(now.get_time())
    print(f"Current State:{light_fsm.current_state}")
    light_fsm.transition(event)
    ## Timer callback every 5 seconds
    event_timer = Timer(1)
    event_timer.init(mode=Timer.PERIODIC, period=5000, callback=timer_callback)


def loop():
    try:
        while True:
            print(f"Current State:{light_fsm.current_state}")
            sleep(30)
    except KeyboardInterrupt:
        event_timer.deinit()
        orb.turn_off()


if __name__ == "__main__":
    setup()
    loop()
