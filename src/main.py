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

def display(enigma):
    display_peripheral = HT16K33Segment14(i2c, board=HT16K33Segment14.SPARKFUN_ALPHA)
    display_peripheral.set_brightness(9)
    display_peripheral.clear()
    display_peripheral.draw()
    display = "    "
    while True:
        for char in enigma.recv():
            display = display[1:] + char
            display_peripheral.clear()
            for i in range(4):
                display_peripheral.set_character(display[i], i)
            display_peripheral.draw()
            sleep(0.1)

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

def reset(enigma):
    GPIO.setup(25, GPIO.IN)
    while True:
        if not GPIO.input(25):
            enigma.send(True)

def enigma(display, led):
    led.send("bbbb")
    print(f"Device: {keyboard.name}, {keyboard.phys}")
    print("Listening for keyboard events...")
    display.send("    ")

    try:
        for event in keyboard.read_loop():
            if event.type == evdev.ecodes.EV_KEY:  # Keyboard event
                key = evdev.ecodes.KEY[event.code]  # Get key name
                if event.value == 1 and key.startswith("KEY_") and len(key)==5:
                    alphanumeric = key[-1]
                    print(alphanumeric, end="")
                    if "0" <= alphanumeric <= "9":
                        display.send(alphanumeric)
    except KeyboardInterrupt:
        print("Keyboard reading stopped.")


    machine = EnigmaMachine(0, 0, 0, 0, 0, 0)
    machine.set_plugboard()
    try:
        for event in keyboard.read_loop():
            if event.type == evdev.ecodes.EV_KEY:  # Keyboard event
                key = evdev.ecodes.KEY[event.code]  # Get key name
                if event.value == 1 and key.startswith("KEY_") and len(key)==5:
                    alphanumeric = key[-1]
                    print(alphanumeric)
                    if "A"<=alphanumeric<="Z":
                        display.send(machine.encrypt(alphanumeric))
                    else:
                        display.send(alphanumeric)
    except KeyboardInterrupt:
        print("Keyboard reading stopped.")

if __name__ == "__main__":
    display_pipe, enigma_pipe_display = Pipe()
    display_process = Process(target=display, args=(display_pipe,))
    display_process.start()

    led_pipe, enigma_pipe_led = Pipe()
    led_process = Process(target=led, args=(led_pipe,))
    led_process.start()

    enigma_process = Process(target=enigma, args=(enigma_pipe_display, enigma_pipe_led))
    enigma_process.start()

    reset_process = Process(target=reset, args=(enigma_process,))
    reset_process.start()

    enigma_process.join()
    display_process.terminate()
    led_process.terminate()
    reset_process.terminate()
