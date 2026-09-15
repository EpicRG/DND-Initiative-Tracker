import customtkinter
import Backend

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("CustomTkinter Test")
root.geometry("450x500")

<<<<<<< HEAD
# Preset players and display settings.
PLAYER_NAMES = ["L", "Mitgalad", "Eran", "Companion"]
DEAD_BUTTON_COLOR = "#555555"
=======
        self.title("DND Initiative Tracker")
        self.geometry("900x700")
>>>>>>> fddd129e31a26e4348183e5621e5c76ade3fba1c

# Application state: widgets are kept so their values can be read later.
player_entries = []
custom_characters = []
dead_characters = set()

# Create the preset-character checkboxes and hidden roll fields.
def creat_checkbox_loop():
    for index, name in enumerate(PLAYER_NAMES):
        player_row = customtkinter.CTkFrame(player_frame)
        player_row.grid(row=index, column=0, columnspan=2, sticky="ew", padx=10, pady=6)
        player_row.grid_columnconfigure(1, weight=1)

        player_checkbox = customtkinter.CTkCheckBox(player_row, text=name)
        player_checkbox.grid(row=0, column=0, sticky="w")

        ask_for_roll = customtkinter.CTkEntry(player_row, placeholder_text="Roll")
        ask_for_roll.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 0))
        ask_for_roll.grid_remove()

        player_row.configure(height=ask_for_roll.cget("height"))
        player_row.grid_propagate(False)
        

        player_checkbox.configure(
            command=lambda checkbox=player_checkbox, entry=ask_for_roll: toggle_button(checkbox, entry)
        )
        player_entries.append((name, player_checkbox, ask_for_roll))

# Show or hide a preset character's roll field.
def toggle_button(checkbox, entry):
    if checkbox.get():
        entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))
    else:
        entry.grid_forget()

    list_character_and_rolls()

# Create the custom-character inputs and control buttons.
def buttons():
    creat_checkbox_loop()

    character_entry = customtkinter.CTkEntry(button_frame, placeholder_text="Enter character name",)
    character_entry.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=6)

    character_roll_entry = customtkinter.CTkEntry(button_frame,placeholder_text="Enter roll",)
    character_roll_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=6)

    reset_button = customtkinter.CTkButton(button_frame, text="Reset", width=90, height=75, fg_color="#B22222", hover_color="#DC143C", command=reset_entries,)
    reset_button.grid(row=2, column=1, columnspan=1, sticky="news", pady=(10, 0), padx=(6, 0))
    
    add_character_button = customtkinter.CTkButton(button_frame, text="Add Character", width=90, height=40, command=lambda: add_character(character_entry, character_roll_entry),)
    add_character_button.grid(row=2, column=0, sticky="news", pady=(10, 0), padx=(6, 0))

    root.bind("<Return>", lambda event:  add_character_button.invoke())
    root.bind("<KP_Enter>", lambda event:  add_character_button.invoke())

def list_character_and_rolls():
    """Read all characters, sort them, and redraw both lists."""
    characters = list(custom_characters)
    for name, checkbox, roll_entry in player_entries:
        if not checkbox.get():
            continue
        try:
            characters.append((name, Backend.parse_roll(name, roll_entry.get().strip())))
        except ValueError as error:
            print(error)
            return

    sorted_characters = Backend.sort_initiative_order(characters)
    active_characters, dead_characters_in_order = Backend.split_dead_characters(sorted_characters,dead_characters,)

    clear_frame(list_frame)
    clear_frame(dead_list_frame)

    for row, character in enumerate(active_characters):
        text = f"{row + 1}. {character[0]} ({character[1]})"
        render_character(list_frame, row, character, text, move_to_dead)

    for row, character in enumerate(dead_characters_in_order):

        text = f"{character[0]} ({character[1]})"
        
        render_character(dead_list_frame, row, character, text, move_to_active, DEAD_BUTTON_COLOR,)

    return sorted_characters

# Remove the old buttons before redrawing a list.
def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()

# Add one clickable character button to a list frame.
def render_character(frame, row, character, text, command, color=None):
    """Create one clickable character button in a list frame."""
    options = {"anchor": "w", "command": lambda: command(character)}
    if color:
        options["fg_color"] = color
    customtkinter.CTkButton(frame, text=text, **options).grid(
        row=row, column=0, sticky="ew", padx=8, pady=4
    )


def move_to_dead(character):
    """Move a character from the active list to the dead list."""
    dead_characters.add(character)
    list_character_and_rolls()


def move_to_active(character):
    """Move a character from the dead list back to the active list."""
    dead_characters.discard(character)
    list_character_and_rolls()

# Validate and store a custom character.
def add_character(name_entry, roll_entry):
    name = name_entry.get().strip()
    roll_text = roll_entry.get().strip()

    if not name or not roll_text:
        print("Enter both a character name and a roll.")
        return

    try:
        roll = Backend.parse_roll(name, roll_text)
    except ValueError as error:
        print(error)
        return

    custom_characters.append((name, roll))

    name_entry.delete(0, "end")
    roll_entry.delete(0, "end")

    list_character_and_rolls()


def reset_entries():
    """Clear custom characters, selected players, and dead status."""
    custom_characters.clear()
    dead_characters.clear()

    for _, checkbox, roll_entry in player_entries:
        checkbox.deselect()
        roll_entry.delete(0, "end")
        roll_entry.grid_remove()

    list_character_and_rolls()


main_frame = customtkinter.CTkFrame(master=root)
main_frame.pack(fill="both", expand=True)

#The fraim all other frames are inn
main_frame.grid_columnconfigure(0, weight=2)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

#Right Panel
button_frame = customtkinter.CTkFrame(master=main_frame)
button_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
button_frame.grid_columnconfigure((0, 1), weight=2)

#Left Panel
player_frame = customtkinter.CTkFrame(master=main_frame, width=200, height=170)
player_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
player_frame.grid_propagate(False)
player_frame.grid_columnconfigure((0, 1), weight=2)

#Bottom left Panel
list_frame = customtkinter.CTkFrame(master=main_frame, width=200, height=300)
list_frame.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
list_frame.grid_columnconfigure(0, weight=1)

#Bottom right Panal
dead_list_frame = customtkinter.CTkFrame(master=main_frame, width=200, height=300)
dead_list_frame.grid(row=1, column=1, sticky="nswe", padx=5, pady=5)
dead_list_frame.grid_columnconfigure(0, weight=1)



def main():
    buttons()
    root.mainloop()
main()
