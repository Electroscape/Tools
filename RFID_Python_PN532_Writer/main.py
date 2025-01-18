from gui import app, action_btns, display_message
import rfid_core as nfc
from time import sleep

def init_nfc(trials=5):
    button = action_btns["init"]
    button_txt = button.cget("text")
    button.config(state="disabled", text="Initializing...")
    count = 0
    assert 20 >= trials >= 0, "Number of trials must be between 0 and 20"
    while count < trials:
        count += 1
        display_message("Init NFC...")
        msg = nfc.init_rfid()
        if msg:
            display_message(msg)
            display_message("NFC Initialized Successfully")
            break
        else:
            display_message(f"NFC Initialization Failed")
            if count < trials:
                display_message(f"Retrying in 1 seconds... ({count}/{trials})")
                sleep(1)
    button.config(text=button_txt, state="normal")


def read_nfc():
    display_message("Read NFC content here.\nCard Type: X\nValue:XX")  # Replace with actual NFC read function

def write_nfc():
    content = app.write_text.get()
    protocol = app.protocol_var.get()
    protocol_name = [name for name, value in nfc.protocol_values.items() if value == protocol][0]
    display_message(f"Writing to NFC: {content} with protocol {protocol_name}")
    print(f"Writing to NFC: {content} with protocol {protocol_name}")  # Replace with actual NFC write function 

# Initialize Action Buttons
action_btns["init"].config(command=init_nfc)
action_btns["read"].config(command=read_nfc)
action_btns["write"].config(command=write_nfc)

# Schedule the function to Initialize NFC after the main loop starts
app.after(1, init_nfc)

# Run the app
app.mainloop()