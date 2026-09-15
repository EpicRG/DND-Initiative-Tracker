import customtkinter
import Backend

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DND Initiative Tracker")
        self.geometry("900x700")

        # Reserve space for the active and dead initiative lists.
        bottom_frame = customtkinter.CTkFrame(master=self)
        bottom_frame.pack(side="bottom", pady=(10, 20), padx=(20, 20), fill="x")
        bottom_frame.configure(height=360)
        # Prevent the frame from shrinking around its children.
        bottom_frame.pack_propagate(False)

        # Keep preset-character controls in a fixed sidebar on the left.
        # master identifies the parent widget that owns this frame.
        left_frame = customtkinter.CTkFrame(master=self)
        left_frame.pack(side="left", pady=(20, 10), padx=(20, 10), fill="y")
        left_frame.grid_columnconfigure(1, weight=1)
        left_frame.sidebar_frame = customtkinter.CTkFrame(left_frame, width=140, corner_radius=0)
        left_content = customtkinter.CTkFrame(master=left_frame, fg_color="transparent")
        left_content.pack(pady=(5, 0), anchor="n")

        # Expand the main area between the sidebar and the leaderboard.
        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=(20, 10), padx=(10, 20), fill="both", expand=True)



        leaderboard_label = customtkinter.CTkLabel(master=bottom_frame, text="Initiative Order", font=("Roboto Medium", 25))
        leaderboard_label.pack(pady=12, padx=10)

        # CTkCanvas is a regular Tk widget, so it needs its background updated
        # manually when CustomTkinter switches between light and dark themes.
        self.order_canvas = customtkinter.CTkCanvas(
            master=bottom_frame,
            height=280,
            highlightthickness=0,
            bg=self._frame_background_color(),
        )
        self.order_canvas.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        # This scrollbar is shown only when more than eight entries exist.
        self.order_scrollbar = customtkinter.CTkScrollbar(
            master=bottom_frame,
            orientation="horizontal",
            command=self.order_canvas.xview,
        )
        self.order_canvas.configure(xscrollcommand=self.order_scrollbar.set)

        # Keep active and dead entries together inside the scrollable canvas.
        self.leaderboard_content = customtkinter.CTkFrame(
            master=self.order_canvas,
            fg_color="transparent",
        )
        self.order_canvas.create_window(
            (0, 0),
            window=self.leaderboard_content,
            anchor="nw",
        )
        self.leaderboard_content.bind(
            "<Configure>",
            # Recalculate the scrollable area whenever the content changes size.
            lambda event: self.order_canvas.configure(
                scrollregion=self.order_canvas.bbox("all")
            ),
        )

        self.order_grid = customtkinter.CTkFrame(master=self.leaderboard_content, fg_color="transparent")
        self.order_grid.pack(fill="x", pady=(4, 8), padx=10)

        dead_label = customtkinter.CTkLabel(master=self.leaderboard_content, text="Dead", font=("Roboto Medium", 20))
        dead_label.pack(pady=(4, 0), padx=10, anchor="w")

        self.dead_grid = customtkinter.CTkFrame(master=self.leaderboard_content, fg_color="transparent")
        self.dead_grid.pack(fill="x", pady=(4, 8), padx=10)

        content_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
        content_frame.place(relx=0.5, y=10, anchor="n")

        title_label = customtkinter.CTkLabel(master=content_frame, text="Initiative Tracker", font=("Roboto Medium", 25))
        title_label.pack(pady=12, padx=10)

        self.order_text = customtkinter.CTkLabel(master=content_frame, text="", font=("Roboto Medium", 16))
        self.order_text.pack(pady=(0, 8), padx=10)

        controls_frame = customtkinter.CTkFrame(master=content_frame, fg_color="transparent")
        controls_frame.pack(anchor="center")


        #Left sidebar with checkboxes and entries for characters

        # Mitgalad
        mitgalad_row = customtkinter.CTkFrame(master=left_content)
        mitgalad_row.pack(anchor="w", pady=6, padx=10)
        mitgalad_row.configure(height=75, width=220)
        mitgalad_row.pack_propagate(False)
        include_mitgalad = customtkinter.CTkCheckBox(master=mitgalad_row, text="Include Mitgalad?")
        include_mitgalad.pack(anchor="w")
        mitgalad_roll_entry = customtkinter.CTkEntry(master=mitgalad_row, placeholder_text="Mitgalad Roll")
        mitgalad_roll_entry.pack_forget()
        # command runs when the checkbox is clicked, after the UI is created.
        include_mitgalad.configure(command=lambda: self.toggle_entry(include_mitgalad, mitgalad_roll_entry))

        # Erran
        erran_row = customtkinter.CTkFrame(master=left_content)
        erran_row.pack(anchor="w", pady=6, padx=10)
        erran_row.configure(height=75, width=220)
        erran_row.pack_propagate(False)
        include_erran = customtkinter.CTkCheckBox(master=erran_row, text="Include Erran?")
        include_erran.pack(anchor="w")
        erran_roll_entry = customtkinter.CTkEntry(master=erran_row, placeholder_text="Erran Roll")
        erran_roll_entry.pack_forget()
        include_erran.configure(command=lambda: self.toggle_entry(include_erran, erran_roll_entry))

        # L
        l_row = customtkinter.CTkFrame(master=left_content)
        l_row.pack(anchor="w", pady=6, padx=10)
        l_row.configure(height=75, width=220)
        l_row.pack_propagate(False)
        include_l = customtkinter.CTkCheckBox(master=l_row, text="Include L?")
        include_l.pack(anchor="w")
        l_roll_entry = customtkinter.CTkEntry(master=l_row, placeholder_text="L Roll")
        l_roll_entry.pack_forget()
        include_l.configure(command=lambda: self.toggle_entry(include_l, l_roll_entry))


        # Controls for adding custom characters one at a time.
        
        name_entry = customtkinter.CTkEntry(master=controls_frame, placeholder_text="Character Name")
        name_entry.pack(pady=6, padx=10)

        roll_entry = customtkinter.CTkEntry(master=controls_frame, placeholder_text="Initiative Roll")
        roll_entry.pack(pady=6, padx=10)

        enter_button = customtkinter.CTkButton(master=controls_frame, text="Enter", command=self.submit_entries,)
        enter_button.pack(pady=6, padx=10)
        self.bind("<Return>", lambda event: enter_button.invoke())
        self.bind("<KP_Enter>", lambda event: enter_button.invoke())

        reset_button = customtkinter.CTkButton(
            master=controls_frame,
            text="Reset",
            command=self.reset_entries,
            fg_color="#B22222",
            hover_color="#DC143C",
        )
        reset_button.pack(pady=6, padx=10)

        self.entries = [
            ("Mitgalad", include_mitgalad, mitgalad_roll_entry),
            ("Erran", include_erran, erran_roll_entry),
            ("L", include_l, l_roll_entry),
        ]
        self.custom_characters = []
        self.dead_characters = set()
        self.name_entry = name_entry
        self.roll_entry = roll_entry

    def _frame_background_color(self):
        frame_colors = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
        return self._apply_appearance_mode(frame_colors)

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        if hasattr(self, "order_canvas"):
            self.order_canvas.configure(bg=self._frame_background_color())


    # Show a preset character's roll field only while its checkbox is selected.
    def toggle_entry(self, checkbox, entry):
        if checkbox.get():
            entry.pack(anchor="w", pady=12, padx=10)
        else:
            entry.pack_forget()
            self.update_leaderboard()

    # Validate and save a custom character, then refresh the leaderboard.
    def submit_entries(self):
        character_name = self.name_entry.get().strip()
        character_roll = self.roll_entry.get().strip()
        if character_name and character_roll:
            try:
                roll = Backend.parse_roll(character_name, character_roll)
            except ValueError as error:
                self.order_text.configure(text=str(error))
                return
        elif character_name or character_roll:
            self.order_text.configure(text="Enter both a character name and a roll.")
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
