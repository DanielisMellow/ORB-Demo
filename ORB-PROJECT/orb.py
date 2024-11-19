import random
from time import sleep


class LEDOrb:
    orb_commands = {
        "B-": 0x04,
        "B+": 0x05,
        "PWR_OFF": 0x06,
        "PWR_ON": 0x07,
    }
    orb_modes = {
        "FLASH": 0x0F,
        "SMOOTH": 0x13,
        "STROBE": 0x17,
        "FADE": 0x1B,
    }
    orb_colors = {
        "G0": 0x08,
        "R0": 0x09,
        "B0": 0x0A,
        "W0": 0x0B,
        "G1": 0x0C,
        "R1": 0x0D,
        "B1": 0x0E,
        "G4": 0x10,
        "R4": 0x11,
        "B4": 0x12,
        "G2": 0x14,
        "R2": 0x15,
        "B2": 0x16,
        "G3": 0x18,
        "R3": 0x19,
        "B3": 0x1A,
    }

    def __init__(self, ir_tx, gate_pin):
        """Requries a configured ir_tx pin uning nec"""
        self.ir_tx = ir_tx
        self.gate_pin = gate_pin

    def turn_on(self, verbose=False):
        orb_colors = list(LEDOrb.orb_colors.values())
        self.gate_pin.on()
        for i in range(2):
            self.ir_tx.transmit(0, LEDOrb.orb_commands["PWR_ON"])

        for i in range(16):
            color_code = random.choice(orb_colors)
            self.ir_tx.transmit(0, color_code)
            sleep(0.5)
        if verbose:
            print("ORB-ON")

    def turn_off(self, verbose=False):
        for i in range(3):
            self.ir_tx.transmit(0, LEDOrb.orb_commands["PWR_OFF"])
            sleep(0.25)
        self.gate_pin.off()
        if verbose:
            print("ORB-OFF")
