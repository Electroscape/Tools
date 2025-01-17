from gui import app, action_btns, display_message
import rfid_core as nfc

def init_nfc():
    action_btns["init"].config(state="disabled")
    count = 1
    while count < 5:
        display_message("Init NFC...\nTrial: " + str(count))
        count += 1
        msg = nfc.init_rfid()
        if msg:
            display_message(msg)
            break
        else:
            display_message(f"NFC Initialization Failed\nRetrying...")
    action_btns["init"].config(state="enabled")


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

app.mainloop()