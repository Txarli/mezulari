import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

# Configurar el LED como salida
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Configurar el teclado HID
keyboard = Keyboard(usb_hid.devices)

# Configurar el pin GP0 como entrada con pull-up
pin = digitalio.DigitalInOut(board.GP0)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.DOWN

# Crear una instancia de Debouncer para el pin GP0
debounced_pin = Debouncer(pin, interval=0.005)

print('Presiona el botón para empezar la grabación')

is_recording = False

while True:
    # Actualizar el estado del Debouncer
    debounced_pin.update()
    
    # Verificar si el pin ha pasado de False a True
    if debounced_pin.fell:
        if is_recording:
            print('Deteniendo la grabación')
            is_recording = False
            keyboard.press(Keycode.S)
            keyboard.release_all()
            keyboard.press(Keycode.ENTER)
            keyboard.release_all()
            led.value = False
        else:
            print('Iniciando la grabación')
            is_recording = True
            keyboard.press(Keycode.CONTROL, Keycode.R)
            keyboard.release_all()
            led.value = True
    
    # Pequeña pausa para evitar un bucle demasiado rápido
    time.sleep(0.1)