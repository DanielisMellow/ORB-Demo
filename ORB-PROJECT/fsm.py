from orb import LEDOrb


class SimpleFSM:
    def __init__(self, light_source: LEDOrb):
        self.states = {
            "bring_up": self.bring_up,
            "on_state": self.on_state,
            "off_state": self.on_state,
            "idle_state": self.idle_state,
        }
        self.current_state = "bring_up"
        self.events = set(
            ["on_trigger_time", "off_trigger_time", "on_time", "other_time"]
        )
        self.light_source = light_source

    def transition(self, event):
        if event in self.events:
            self.current_state = self.states[self.current_state](event)
        else:
            print(f"Invalid event: {event}")

    def bring_up(self, event):
        if event == "on_time" or event == "on_trigger_time":
            self.current_state = "on_state"
            # On sequence
            self.light_source.turn_on()
        else:
            self.current_state = "off_state"
            # Off sequence
            self.light_source.turn_off()
        return self.current_state

    def on_state(self, event):
        if event == "other_time":
            self.current_state = "idle_state"
            # Idle sequence
        return self.current_state

    def off_state(self, event):
        if event == "other_time":
            self.current_state = "idle_state"
            # Idle sequence
        return self.current_state

    def idle_state(self, event):
        if event == "on_trigger_time":
            self.current_state = "on_state"
            # ON sequence
            self.light_source.turn_on()
        elif event == "off_trigger_time":
            self.current_state = "off_state"
            # OFF sequence
            self.light_source.turn_off()
        return self.current_state
