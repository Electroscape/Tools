from gui import (app, action_btns, protocol_values, display_message,
                 clear_display, set_btns_to_default, set_write_values, get_write_values, show_overlay, cancel_overlay)
from rfid_core import init_rfid, get_rfid_configurations,  rfid_present, rfid_read, authenticate, rfid_write
from time import sleep

# Global Variables
pn532 = None
cancel_state = {"cancelled_by_user": False}

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
            # Get configuration from the NFC device
            msg = get_rfid_configurations(pn532)
            display_message(msg)
            display_message("NFC Initialized Successfully")
            break
        else:
            display_message(f"NFC Initialization Failed")
            if count < trials:
                display_message(
                    f"Retrying in 1 seconds... ({count}/{trials})\n")
                sleep(1)
    
    set_btns_to_default(default_btns)


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

    # Show overlay gray box with text "Place card on the reader"
    show_overlay(cancel_state, on_cancel=lambda: print("NFC read canceled by user."))

    while not cancel_state["cancelled_by_user"]:
        sleep(0.05)
        app.update()
        # Wait for card to be present
        card_uid = rfid_present(pn532)

        # Card detected
        if card_uid:
            cancel_overlay(cancel_state, on_cancel=lambda: print("NFC read canceled by user."))

            display_message(f"Card detected, reading data...")
            print(f"Card found uid: {card_uid}")

            card_read = rfid_read(card_uid, pn532)
            protocol = "Classic" if authenticate(card_uid, pn532) else "NTAG"

            display_message(
                f"Data on card: '{card_read}', Card Type: {protocol}")
            print(f"Data on card: '{card_read}', Card Type: {protocol}")

            set_write_values(card_read, protocol_values[protocol])

            if card_read == "x":
                print(f"Unless you wrote '{card_read}' , please try again")
                display_message(
                    f"Unless you wrote '{card_read}', please try again")

            button.config(text=button_txt, state="normal")
            return True
        
    display_message("NFC read canceled by user.")
    button.config(text=button_txt, state="normal")
    return False


def gui_write_nfc():
    clear_display()
    content, protocol = get_write_values()
    if not pn532:
        display_message("NFC not initialized, please initialize first.")
        return False
    elif not protocol < 9:
        display_message(
            "Cannot write to NFC with protocol 'Auto', please select a protocol")
        display_message("Check card type via 'Read' and try again")
        return False
    elif not content:
        display_message(
            "Text field is empty, please enter text to write to the NFC card")
        return False
    
    button = action_btns["write"]
    button_txt = button.cget("text")
    button.config(state="disabled", text="Writing...")
    
    display_message("Writing to NFC...")
    display_message("Place card on the reader...")
    
    # Show overlay gray box with text "Place card on the reader"
    show_overlay(cancel_state, on_cancel=lambda: print("NFC read canceled by user."))

    while not cancel_state["cancelled_by_user"]:
        sleep(0.05)
        app.update()
        # Wait for card to be present
        card_uid = rfid_present(pn532)

        # Card detected
        if card_uid:
            cancel_overlay(cancel_state, on_cancel=lambda: print("Card detected"))

            display_message(f"Card detected, writing data...")
            print(f"Card found uid: {card_uid}")
            protocol_name = [
                name for name, value in protocol_values.items() if value == protocol][0]
            print(f"Writing to card: {content} with protocol {protocol_name}")
            display_message(
                f"Writing to NFC: '{content}' with protocol {protocol_name}")

            is_success = rfid_write(pn532, content, protocol)
            if is_success:
                display_message("Data written successfully")
                print("Data written successfully")
                app.after(1000, gui_read_nfc)
            else:
                display_message("Failed to write data")
                print("Failed to write data")

            break
    if cancel_state["cancelled_by_user"]:
        display_message("NFC write canceled by user.")
    button.config(text=button_txt, state="normal")


# Initialize Action Buttons
default_btns = {
    "init": {"text": "Init NFC", "command": gui_init_nfc},
    "read": {"text": "Read Card", "command": gui_read_nfc},
    "write": {"text": "Write", "command": gui_write_nfc}
}

set_btns_to_default(default_btns)

# Schedule the function to Initialize NFC after the main loop starts
app.after(1, gui_init_nfc)

# Run the app
app.mainloop()
