from gui import app, action_btns, protocol_values, display_message, clear_display, set_write_values
from rfid_core import init_rfid, get_rfid_configurations,  rfid_present, rfid_read, authenticate
from time import sleep

# Global Variables
pn532 = None

def gui_init_nfc(trials=5):
    clear_display()
    global pn532

    button = action_btns["init"]
    button_txt = button.cget("text")
    button.config(state="disabled", text="Initializing...")
    count = 0
    assert 20 >= trials >= 0, "Number of trials must be between 0 and 20"
    while count < trials:
        count += 1
        display_message("Init NFC...")
        pn532 = init_rfid()
        if pn532:
            msg = get_rfid_configurations(pn532) # Get configuration from the NFC device
            display_message(msg)
            display_message("NFC Initialized Successfully")
            break
        else:
            display_message(f"NFC Initialization Failed")
            if count < trials:
                display_message(f"Retrying in 1 seconds... ({count}/{trials})\n")
                sleep(1)
    button.config(text=button_txt, state="normal")


def gui_read_nfc() -> bool:
    clear_display()
    if not pn532:
        display_message("NFC not initialized, please initialize first.")
        return False
    
    button = action_btns["read"]
    button_txt = button.cget("text")
    button.config(state="disabled", text="Reading...")
    
    display_message("Reading NFC...")
    display_message("Place card on the reader...")
    while True:
        sleep(0.05)
        # Wait for card to be present
        card_uid = rfid_present(pn532)

        # Card detected
        if card_uid:
            display_message(f"Card detected, reading data...")
            print(f"Card found uid: {card_uid}")

            card_read = rfid_read(card_uid, pn532)
            protocol = "Classic" if authenticate(card_uid, pn532) else "NTAG"
            
            display_message(f"Data on card: '{card_read}', Card Type: {protocol}")
            print(f"Data on card: '{card_read}', Card Type: {protocol}")

            set_write_values(card_read, protocol_values[protocol])

            # wait here until card is removed
            display_message("Please remove card, waiting for card removal...")
            current_card = rfid_present(pn532)
            if card_read != "x":
                while current_card and current_card == rfid_present(pn532):
                    continue
            
                # Return to default value
                display_message("Card removed")
                print("card removed")
                button.config(text=button_txt, state="normal")
                return True
            else:
                print(f"Unless you wrote '{card_read}' , please try again")
                display_message(f"Unless you wrote '{card_read}', please try again")
                button.config(text=button_txt, state="normal")
                return False

def gui_write_nfc():
    content = app.write_text.get()
    protocol = app.protocol_var.get()
    protocol_name = [name for name, value in protocol_values.items() if value == protocol][0]
    display_message(f"Writing to NFC: {content} with protocol {protocol_name}")
    print(f"Writing to NFC: {content} with protocol {protocol_name}")  # Replace with actual NFC write function 

# Initialize Action Buttons
action_btns["init"].config(command=gui_init_nfc)
action_btns["read"].config(command=gui_read_nfc)
action_btns["write"].config(command=gui_write_nfc)

# Schedule the function to Initialize NFC after the main loop starts
app.after(1, gui_init_nfc)

# Run the app
app.mainloop()