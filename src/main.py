from board import SCL, SDA
from busio import I2C
from time import sleep
from datetime import datetime
from multiprocessing import Process, Pipe
import RPi.GPIO as GPIO
from ht16k33 import HT16K33Segment14
from EnigmaMachine import EnigmaMachine
import evdev

i2c = I2C(SCL, SDA)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

keyboard = evdev.InputDevice('/dev/input/by-id/usb-Dell_Dell_Wired_Multimedia_Keyboard-event-kbd')

def display(enigma, replay, replay_read):
    display_peripheral = HT16K33Segment14(i2c, board=HT16K33Segment14.SPARKFUN_ALPHA)
    display_peripheral.set_brightness(9)
    display_peripheral.clear()
    display_peripheral.draw()
    display = "    "
    while True:
        if enigma.poll(0.001):
            for char in enigma.recv():
                display = display + char
                display_peripheral.clear()
                if char == "|":
                    display = "    "
                for i in range(4):
                    display_peripheral.set_character(display[i-4], i)
                display_peripheral.draw()
                if char == "|":
                    display = "    "
                sleep(0.01)
        elif replay.poll(0.001):
            replay_read.send(True)
            replay.recv()
            for i in range(len(display)-3):
                display_peripheral.clear()
                for j in range(4):
                    display_peripheral.set_character(display[i+j], j)
                display_peripheral.draw()
                sleep(0.33)

def led(enigma):
    gpio = [21, 20, 16, 12]
    for i in gpio:
        GPIO.setup(i, GPIO.OUT)
    led = "ffff"
    while True:
        if enigma.poll(0.001):
            temp = enigma.recv()
            if len(temp) == 4:
                led = temp
        for i, char in enumerate(led):
            if char == "n" or (char == "b" and datetime.now().microsecond // 100000 < 5):
                GPIO.output(gpio[i], True)
            elif char == "f" or (char == "b" and not datetime.now().microsecond // 100000 < 5):
                GPIO.output(gpio[i], False)

def replay(display, display_read):
    GPIO.setup(25, GPIO.IN)
    sent = False
    pre = False
    while True:
        now = GPIO.input(25)
        if pre and not now and not sent:
            sent = True
            display.send(True)
        if display_read.poll(0.001):
            display_read.recv()
            sent = False
        pre = now

def reset(enigma, enigma_read):
    GPIO.setup(24, GPIO.IN)
    sent = False
    pre = False
    while True:
        now = GPIO.input(24)
        if pre and not now and not sent:
            sent = True
            enigma.send(True)
        if enigma_read.poll(0.001):
            enigma_read.recv()
            sent = False
        pre = now

def enigma(display, led, reset, reset_read):
    while True:
        # Reset
        if reset.poll(0.001):
            reset_read.send(True)
            reset.recv()
        led.send("ffff")
        display.send("|")

        # Set the first router
        led.send("bfff")
        letter = get_letter(reset)
        if not letter:
            continue
        first_rotor_position = ord(letter) - ord('A')
        print(f"The first router: {first_rotor_position}")

        # Set the second router
        led.send("nbff")
        letter = get_letter(reset)
        if not letter:
            continue
        second_rotor_position = ord(letter) - ord('A')
        print(f"The second router: {second_rotor_position}")

        # Set the third router
        led.send("nnbf")
        letter = get_letter(reset)
        if not letter:
            continue
        third_rotor_position = ord(letter) - ord('A')
        print(f"The third router: {third_rotor_position}")

        led.send("nnnn")
        machine = EnigmaMachine(first_rotor_position, second_rotor_position, third_rotor_position)
        machine.set_plugboard()
        while not reset.poll(0.001):
            letter = get_letter(reset)
            if not letter:
                break
            encrypted = machine.encrypt(letter)
            print(f"{letter} => {encrypted}")
            display.send(encrypted)

def get_letter(reset):
    while not reset.poll(0.001):
        event = keyboard.read_one()
        if event and event.type == evdev.ecodes.EV_KEY:  # Keyboard event
            key = evdev.ecodes.KEY[event.code]  # Get key name
            if event.value == 1 and key.startswith("KEY_") and len(key)==5:
                alphanumeric = key[-1]
                if "A" <= alphanumeric <= "Z":
                    return alphanumeric

if __name__ == "__main__":
    display_pipe, enigma_pipe_display = Pipe()
    replay_pipe, display_pipe_replay = Pipe()
    replay_read_pipe, display_pipe_replay_read = Pipe()
    display_process = Process(target=display, args=(display_pipe, display_pipe_replay, display_pipe_replay_read))
    display_process.start()

    led_pipe, enigma_pipe_led = Pipe()
    led_process = Process(target=led, args=(led_pipe,))
    led_process.start()

    reset_pipe, enigma_pipe_reset = Pipe()
    reset_read_pipe, enigma_pipe_reset_read = Pipe()
    enigma_process = Process(target=enigma, args=(enigma_pipe_display, enigma_pipe_led, enigma_pipe_reset, enigma_pipe_reset_read))
    enigma_process.start()

    reset_process = Process(target=reset, args=(reset_pipe, reset_read_pipe))
    reset_process.start()

    replay_process = Process(target=replay, args=(replay_pipe, replay_read_pipe))
    replay_process.start()

    enigma_process.join()
    display_process.terminate()
    led_process.terminate()
    reset_process.terminate()
