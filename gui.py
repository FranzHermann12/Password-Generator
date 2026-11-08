
"""
Password Generator
Classic Windows Desktop Interface
Version: 1.5.0
Developer: Franz_Hermann1
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

from generator import PasswordConfig, PasswordGenerator
from config import AppConfig, ConfigManager
from profiles import ProfileManager
from strength import PasswordAnalyzer


class PasswordGeneratorGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("700x530")
        self.root.minsize(650, 480)
        self.root.configure(bg="#d4d0c8")

        self.bg = "#d4d0c8"
        self.font = ("MS Sans Serif", 8)

        self.app_config = ConfigManager.load()

        self.uppercase = tk.BooleanVar(value=self.app_config.uppercase)
        self.lowercase = tk.BooleanVar(value=self.app_config.lowercase)
        self.numbers = tk.BooleanVar(value=self.app_config.numbers)
        self.symbols = tk.BooleanVar(value=self.app_config.symbols)

        self.exclude_similar = tk.BooleanVar(
            value=self.app_config.exclude_similar
        )
        self.exclude_ambiguous = tk.BooleanVar(
            value=self.app_config.exclude_ambiguous
        )

        self.length = tk.StringVar(
            value=str(self.app_config.default_length)
        )
        self.quantity = tk.StringVar(
            value=str(self.app_config.default_quantity)
        )

        self.custom_symbols = tk.StringVar(
            value=self.app_config.custom_symbols
        )
        self.excluded_characters = tk.StringVar(
            value=self.app_config.excluded_characters
        )
        self.required_characters = tk.StringVar(
            value=self.app_config.required_characters
        )

        self.show_password_analysis = tk.BooleanVar(
            value=self.app_config.show_password_analysis
        )
        self.show_entropy = tk.BooleanVar(
            value=self.app_config.show_entropy
        )

        # Password visibility
        self.passwords_visible = False
        self.generated_passwords = []
        self.last_pool_size = None

        self.create_menu()
        self.create_interface()
        self.select_tab("Generate")

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # --------------------------------------------------
    # MENU
    # --------------------------------------------------

    def create_menu(self):

        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Generate", command=self.generate)
        file_menu.add_command(label="Copy", command=self.copy_passwords)
        file_menu.add_separator()
        file_menu.add_command(
            label="Save Settings",
            command=self.save_settings
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.close_application
        )

        options_menu = tk.Menu(menu, tearoff=0)
        options_menu.add_command(
            label="Reset Settings",
            command=self.restore_defaults
        )

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)

        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Options", menu=options_menu)
        menu.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu)

    # --------------------------------------------------
    # INTERFACE
    # --------------------------------------------------

    def create_interface(self):

        navigation = tk.Frame(self.root, bg=self.bg)
        navigation.pack(fill="x", padx=8, pady=8)

        self.navigation_buttons = {}

        tabs = [
            "Generate",
            "Customize",
            "Profiles",
            "Analysis",
            "Settings"
        ]

        for tab in tabs:

            button = tk.Button(
                navigation,
                text=tab,
                width=12,
                font=self.font,
                relief="raised",
                bd=2,
                command=lambda name=tab: self.select_tab(name)
            )

            button.pack(side="left", padx=1)
            self.navigation_buttons[tab] = button

        self.page_container = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.page_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.generate_page = tk.Frame(
            self.page_container, bg=self.bg
        )
        self.customize_page = tk.Frame(
            self.page_container, bg=self.bg
        )
        self.profiles_page = tk.Frame(
            self.page_container, bg=self.bg
        )
        self.analysis_page = tk.Frame(
            self.page_container, bg=self.bg
        )
        self.settings_page = tk.Frame(
            self.page_container, bg=self.bg
        )

        self.create_generate_page()
        self.create_customize_page()
        self.create_profiles_page()
        self.create_analysis_page()
        self.create_settings_page()

        self.status = tk.Label(
            self.root,
            text="Ready",
            font=self.font,
            bg=self.bg,
            anchor="w",
            relief="sunken",
            bd=1
        )

        self.status.pack(
            fill="x",
            side="bottom",
            padx=8,
            pady=5
        )

    # --------------------------------------------------
    # GENERATE PAGE
    # --------------------------------------------------

    def create_generate_page(self):

        presets = tk.LabelFrame(
            self.generate_page,
            text="Password Presets",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        presets.pack(fill="x", pady=(0, 8))

        for name in [
            "Standard", "Strong", "PIN", "Easy Read", "Custom"
        ]:

            tk.Button(
                presets,
                text=name,
                width=11,
                font=self.font,
                command=lambda preset=name: self.apply_preset(preset)
            ).pack(side="left", padx=3, pady=5)

        settings = tk.LabelFrame(
            self.generate_page,
            text="Generation Settings",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        settings.pack(fill="x", pady=(0, 8))

        tk.Label(
            settings,
            text="Password length:",
            font=self.font,
            bg=self.bg
        ).grid(row=0, column=0, padx=8, pady=7)

        tk.Entry(
            settings,
            textvariable=self.length,
            width=10,
            font=self.font
        ).grid(row=0, column=1, padx=5)

        tk.Label(
            settings,
            text="Quantity:",
            font=self.font,
            bg=self.bg
        ).grid(row=0, column=2, padx=8)

        tk.Entry(
            settings,
            textvariable=self.quantity,
            width=10,
            font=self.font
        ).grid(row=0, column=3, padx=5)

        output_frame = tk.LabelFrame(
            self.generate_page,
            text="Generated Passwords",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        output_frame.pack(fill="both", expand=True)

        output_container = tk.Frame(output_frame, bg=self.bg)
        output_container.pack(
            fill="both", expand=True, padx=5, pady=5
        )

        scrollbar = tk.Scrollbar(output_container)
        scrollbar.pack(side="right", fill="y")

        self.output_listbox = tk.Listbox(
            output_container,
            font=("Courier New", 10),
            selectmode="extended",
            yscrollcommand=scrollbar.set,
            relief="sunken",
            bd=2
        )
        self.output_listbox.pack(
            side="left", fill="both", expand=True
        )

        scrollbar.config(command=self.output_listbox.yview)

        buttons = tk.Frame(self.generate_page, bg=self.bg)
        buttons.pack(fill="x", pady=8)

        tk.Button(
            buttons,
            text="Generate",
            width=12,
            font=self.font,
            command=self.generate
        ).pack(side="left", padx=2)

        tk.Button(
            buttons,
            text="Copy Selected",
            width=13,
            font=self.font,
            command=self.copy_passwords
        ).pack(side="left", padx=2)

        tk.Button(
            buttons,
            text="Show Passwords",
            width=14,
            font=self.font,
            command=self.toggle_visibility
        ).pack(side="left", padx=2)

        self.visibility_button = buttons.winfo_children()[-1]

        tk.Button(
            buttons,
            text="Clear Output",
            width=12,
            font=self.font,
            command=self.clear_output
        ).pack(side="left", padx=2)

    # --------------------------------------------------
    # PASSWORD VISIBILITY
    # --------------------------------------------------

    def refresh_output(self):

        selected = self.output_listbox.curselection()

        self.output_listbox.delete(0, tk.END)

        for password in self.generated_passwords:

            if self.passwords_visible:
                displayed = password
            else:
                displayed = "*" * len(password)

            self.output_listbox.insert(tk.END, displayed)

        for index in selected:
            if index < len(self.generated_passwords):
                self.output_listbox.selection_set(index)

    def toggle_visibility(self):

        if not self.generated_passwords:
            messagebox.showinfo(
                "Password Visibility",
                "Generate passwords first."
            )
            return

        self.passwords_visible = not self.passwords_visible

        self.refresh_output()

        if self.passwords_visible:

            self.visibility_button.config(
                text="Hide Passwords"
            )
            self.status.config(text="Passwords are visible.")

        else:

            self.visibility_button.config(
                text="Show Passwords"
            )
            self.status.config(text="Passwords are hidden.")

    # --------------------------------------------------
    # CUSTOMIZE PAGE
    # --------------------------------------------------

    def create_customize_page(self):

        options_frame = tk.LabelFrame(
            self.customize_page,
            text="Character Options",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        options_frame.pack(fill="x", pady=(0, 8))

        options = [
            ("Uppercase letters (A-Z)", self.uppercase),
            ("Lowercase letters (a-z)", self.lowercase),
            ("Numbers (0-9)", self.numbers),
            ("Symbols", self.symbols),
            ("Exclude similar characters", self.exclude_similar),
            ("Exclude ambiguous characters", self.exclude_ambiguous)
        ]

        for label, variable in options:

            tk.Checkbutton(
                options_frame,
                text=label,
                variable=variable,
                font=self.font,
                bg=self.bg,
                anchor="w"
            ).pack(fill="x", padx=8, pady=3)

        characters_frame = tk.LabelFrame(
            self.customize_page,
            text="Custom Characters",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        characters_frame.pack(fill="x", pady=5)

        fields = [
            ("Custom symbols:", self.custom_symbols),
            ("Excluded characters:", self.excluded_characters),
            ("Required characters:", self.required_characters)
        ]

        for row, (label, variable) in enumerate(fields):

            tk.Label(
                characters_frame,
                text=label,
                font=self.font,
                bg=self.bg
            ).grid(row=row, column=0, sticky="w", padx=8, pady=7)

            tk.Entry(
                characters_frame,
                textvariable=variable,
                font=self.font,
                width=35
            ).grid(row=row, column=1, sticky="ew", padx=8, pady=5)

        characters_frame.columnconfigure(1, weight=1)

        tk.Button(
            self.customize_page,
            text="Reset Settings",
            width=15,
            font=self.font,
            command=self.restore_defaults
        ).pack(anchor="w", pady=10)

    # --------------------------------------------------
    # PROFILES PAGE
    # --------------------------------------------------

    def create_profiles_page(self):

        profile_frame = tk.LabelFrame(
            self.profiles_page,
            text="Saved Password Profiles",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        profile_frame.pack(fill="both", expand=True, pady=5)

        self.profile_listbox = tk.Listbox(
            profile_frame,
            font=self.font,
            selectmode="browse",
            relief="sunken",
            bd=2
        )
        self.profile_listbox.pack(
            fill="both", expand=True, padx=8, pady=8
        )

        buttons = tk.Frame(self.profiles_page, bg=self.bg)
        buttons.pack(fill="x", pady=8)

        tk.Button(
            buttons,
            text="Save Profile",
            width=14,
            font=self.font,
            command=self.save_profile
        ).pack(side="left", padx=3)

        tk.Button(
            buttons,
            text="Load Profile",
            width=14,
            font=self.font,
            command=self.load_profile
        ).pack(side="left", padx=3)

        tk.Button(
            buttons,
            text="Delete Profile",
            width=14,
            font=self.font,
            command=self.delete_profile
        ).pack(side="left", padx=3)

        tk.Button(
            buttons,
            text="Refresh",
            width=12,
            font=self.font,
            command=self.refresh_profiles
        ).pack(side="left", padx=3)

        self.refresh_profiles()

    # --------------------------------------------------
    # ANALYSIS PAGE
    # --------------------------------------------------

    def create_analysis_page(self):

        tk.Label(
            self.analysis_page,
            text="Password Analysis",
            font=("MS Sans Serif", 11, "bold"),
            bg=self.bg
        ).pack(anchor="w", pady=(5, 8))

        tk.Label(
            self.analysis_page,
            text=(
                "Select generated passwords on the Generate page, "
                "then analyze them here."
            ),
            font=self.font,
            bg=self.bg,
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=5)

        tk.Button(
            self.analysis_page,
            text="Analyze Selected Passwords",
            width=25,
            font=self.font,
            command=self.analyze_selected
        ).pack(anchor="w", pady=8)

        result_frame = tk.LabelFrame(
            self.analysis_page,
            text="Analysis Results",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        result_frame.pack(fill="both", expand=True, pady=5)

        self.analysis_text = tk.Text(
            result_frame,
            font=("Courier New", 9),
            bg="white",
            relief="sunken",
            bd=2,
            wrap="word",
            height=12
        )
        self.analysis_text.pack(
            fill="both", expand=True, padx=5, pady=5
        )

        self.analysis_text.insert(
            tk.END, "No analysis available yet."
        )
        self.analysis_text.config(state="disabled")

    # --------------------------------------------------
    # SETTINGS PAGE
    # --------------------------------------------------

    def create_settings_page(self):

        tk.Label(
            self.settings_page,
            text="Application Settings",
            font=("MS Sans Serif", 11, "bold"),
            bg=self.bg
        ).pack(anchor="w", pady=12)

        display_frame = tk.LabelFrame(
            self.settings_page,
            text="Display Options",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        display_frame.pack(fill="x", pady=5)

        tk.Checkbutton(
            display_frame,
            text="Enable password analysis",
            variable=self.show_password_analysis,
            font=self.font,
            bg=self.bg
        ).pack(anchor="w", padx=8, pady=5)

        tk.Checkbutton(
            display_frame,
            text="Show entropy in analysis reports",
            variable=self.show_entropy,
            font=self.font,
            bg=self.bg
        ).pack(anchor="w", padx=8, pady=5)

        info_frame = tk.LabelFrame(
            self.settings_page,
            text="Application Information",
            font=self.font,
            bg=self.bg,
            bd=2
        )
        info_frame.pack(fill="x", pady=8)

        for info in [
            "Application: Password Generator",
            "Version: 1.5.0",
            "Developer: Franz_Hermann1"
        ]:

            tk.Label(
                info_frame,
                text=info,
                font=self.font,
                bg=self.bg
            ).pack(anchor="w", padx=8, pady=4)

        buttons = tk.Frame(self.settings_page, bg=self.bg)
        buttons.pack(anchor="w", pady=12)

        tk.Button(
            buttons,
            text="Save Settings",
            width=15,
            font=self.font,
            command=self.save_settings
        ).pack(side="left", padx=3)

        tk.Button(
            buttons,
            text="Restore Defaults",
            width=15,
            font=self.font,
            command=self.restore_defaults
        ).pack(side="left", padx=3)

    # --------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------

    def select_tab(self, selected):

        for name, button in self.navigation_buttons.items():

            button.config(
                relief="sunken" if name == selected else "raised"
            )

        pages = {
            "Generate": self.generate_page,
            "Customize": self.customize_page,
            "Profiles": self.profiles_page,
            "Analysis": self.analysis_page,
            "Settings": self.settings_page
        }

        for page in pages.values():
            page.pack_forget()

        pages[selected].pack(fill="both", expand=True)

        if selected == "Profiles":
            self.refresh_profiles()

    # --------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------

    def get_app_config(self):

        return AppConfig(
            default_length=int(self.length.get()),
            default_quantity=int(self.quantity.get()),

            uppercase=self.uppercase.get(),
            lowercase=self.lowercase.get(),
            numbers=self.numbers.get(),
            symbols=self.symbols.get(),

            custom_symbols=self.custom_symbols.get(),
            excluded_characters=self.excluded_characters.get(),
            required_characters=self.required_characters.get(),

            exclude_similar=self.exclude_similar.get(),
            exclude_ambiguous=self.exclude_ambiguous.get(),

            show_password_analysis=self.show_password_analysis.get(),
            show_entropy=self.show_entropy.get()
        )

    def apply_app_config(self, config):

        self.length.set(str(config.default_length))
        self.quantity.set(str(config.default_quantity))

        self.uppercase.set(config.uppercase)
        self.lowercase.set(config.lowercase)
        self.numbers.set(config.numbers)
        self.symbols.set(config.symbols)

        self.custom_symbols.set(config.custom_symbols)
        self.excluded_characters.set(config.excluded_characters)
        self.required_characters.set(config.required_characters)

        self.exclude_similar.set(config.exclude_similar)
        self.exclude_ambiguous.set(config.exclude_ambiguous)

        self.show_password_analysis.set(
            config.show_password_analysis
        )
        self.show_entropy.set(config.show_entropy)

    def save_settings(self):

        try:

            config = self.get_app_config()
            ConfigManager.save(config)
            self.app_config = config

            self.status.config(text="Application settings saved.")

            messagebox.showinfo(
                "Settings",
                "Your settings have been saved successfully."
            )

        except (ValueError, TypeError, OSError) as error:

            messagebox.showerror("Settings Error", str(error))

    def restore_defaults(self):

        defaults = AppConfig()
        self.apply_app_config(defaults)

        self.status.config(
            text="Default settings restored. Save to keep them."
        )

    def close_application(self):

        try:
            ConfigManager.save(self.get_app_config())

        except (ValueError, TypeError, OSError) as error:

            messagebox.showerror(
                "Settings Error",
                f"Could not save settings:\n{error}"
            )
            return

        self.root.destroy()

    # --------------------------------------------------
    # PROFILE OPERATIONS
    # --------------------------------------------------

    def refresh_profiles(self):

        self.profile_listbox.delete(0, tk.END)

        for name in ProfileManager.list_profiles():
            self.profile_listbox.insert(tk.END, name)

    def save_profile(self):

        try:

            settings = self.get_app_config()

            name = simpledialog.askstring(
                "Save Profile",
                "Enter a name for this profile:",
                parent=self.root
            )

            if name is None:
                return

            ProfileManager.save_profile(name, settings)
            self.refresh_profiles()

            self.status.config(
                text=f"Profile '{name.strip()}' saved."
            )

        except (ValueError, TypeError, OSError) as error:

            messagebox.showerror("Save Profile Error", str(error))

    def load_profile(self):

        selected = self.profile_listbox.curselection()

        if not selected:

            messagebox.showwarning(
                "Load Profile",
                "Select a profile first."
            )
            return

        name = self.profile_listbox.get(selected[0])

        try:

            config = ProfileManager.load_profile(name)
            self.apply_app_config(config)

            self.status.config(text=f"Loaded profile: {name}")
            self.select_tab("Generate")

        except (ValueError, TypeError) as error:

            messagebox.showerror("Load Profile Error", str(error))

    def delete_profile(self):

        selected = self.profile_listbox.curselection()

        if not selected:

            messagebox.showwarning(
                "Delete Profile",
                "Select a profile first."
            )
            return

        name = self.profile_listbox.get(selected[0])

        confirm = messagebox.askyesno(
            "Delete Profile",
            f"Delete the profile '{name}'?"
        )

        if not confirm:
            return

        try:

            ProfileManager.delete_profile(name)
            self.refresh_profiles()

            self.status.config(text=f"Deleted profile: {name}")

        except (ValueError, OSError) as error:

            messagebox.showerror("Delete Profile Error", str(error))

    # --------------------------------------------------
    # GENERATION
    # --------------------------------------------------

    def generate(self):

        try:

            config = PasswordConfig(
                length=int(self.length.get()),
                quantity=int(self.quantity.get()),

                uppercase=self.uppercase.get(),
                lowercase=self.lowercase.get(),
                numbers=self.numbers.get(),
                symbols=self.symbols.get(),

                custom_symbols=self.custom_symbols.get(),
                excluded_characters=self.excluded_characters.get(),
                required_characters=self.required_characters.get(),

                exclude_similar=self.exclude_similar.get(),
                exclude_ambiguous=self.exclude_ambiguous.get()
            )

            generator = PasswordGenerator(config)

            passwords = generator.generate_multiple()
            pool_size = generator.get_character_pool_size()

            self.generated_passwords = passwords
            self.passwords_visible = False
            self.last_pool_size = pool_size

            self.visibility_button.config(
                text="Show Passwords"
            )

            self.refresh_output()

            self.status.config(
                text=f"Generated {len(passwords)} passwords | "
                     f"Character pool: {pool_size}"
            )

        except (ValueError, TypeError) as error:

            messagebox.showerror("Generation Error", str(error))

    # --------------------------------------------------
    # PASSWORD ANALYSIS
    # --------------------------------------------------

    def analyze_selected(self):

        if not self.show_password_analysis.get():

            messagebox.showinfo(
                "Password Analysis",
                "Password analysis is disabled in Settings."
            )
            return

        selected = self.output_listbox.curselection()

        if not selected:

            messagebox.showwarning(
                "Password Analysis",
                "Select at least one generated password."
            )
            return

        if self.last_pool_size is None:
            messagebox.showwarning(
                "Password Analysis",
                "Generate passwords first."
            )
            return

        self.analysis_text.config(state="normal")
        self.analysis_text.delete("1.0", tk.END)

        try:

            for number, index in enumerate(selected, start=1):

                password = self.generated_passwords[index]

                report = PasswordAnalyzer.analyze(
                    password,
                    self.last_pool_size
                )

                digits = str(report.search_space)

                if len(digits) <= 12:
                    search_display = f"{report.search_space:,}"
                else:
                    search_display = (
                        f"{digits[0]}.{digits[1:4]} "
                        f"x 10^{len(digits) - 1}"
                    )

                entropy_display = ""

                if self.show_entropy.get():
                    entropy_display = (
                        f"Estimated entropy: "
                        f"{report.entropy_bits} bits\n"
                    )

                self.analysis_text.insert(
                    tk.END,
                    f"PASSWORD {number}\n"
                    f"{'-' * 38}\n"
                    f"Length: {report.length}\n"
                    f"Character pool size: "
                    f"{report.character_pool_size}\n"
                    f"{entropy_display}"
                    f"Estimated search space: "
                    f"{search_display}\n"
                    f"Strength classification: "
                    f"{report.strength}\n\n"
                    f"Note: {report.analysis_note}\n\n"
                    f"{'=' * 38}\n\n"
                )

            self.status.config(
                text=f"Analyzed {len(selected)} password(s)."
            )

        except (ValueError, TypeError, IndexError) as error:

            messagebox.showerror("Analysis Error", str(error))

        finally:
            self.analysis_text.config(state="disabled")

    # --------------------------------------------------
    # PRESETS
    # --------------------------------------------------

    def apply_preset(self, preset):

        if preset == "Standard":

            self.restore_defaults()
            self.length.set("20")
            self.quantity.set("5")

        elif preset == "Strong":

            self.restore_defaults()
            self.length.set("32")
            self.quantity.set("5")

        elif preset == "PIN":

            self.length.set("8")
            self.quantity.set("5")

            self.uppercase.set(False)
            self.lowercase.set(False)
            self.numbers.set(True)
            self.symbols.set(False)

            self.exclude_similar.set(False)
            self.exclude_ambiguous.set(False)

        elif preset == "Easy Read":

            self.length.set("16")
            self.quantity.set("5")

            self.uppercase.set(True)
            self.lowercase.set(True)
            self.numbers.set(True)
            self.symbols.set(False)

            self.exclude_similar.set(True)
            self.exclude_ambiguous.set(True)

        elif preset == "Custom":

            self.select_tab("Customize")

        self.status.config(text=f"Selected preset: {preset}")

    # --------------------------------------------------
    # OTHER FUNCTIONS
    # --------------------------------------------------

    def copy_passwords(self):

        selected = self.output_listbox.curselection()

        if not selected:

            messagebox.showwarning(
                "Copy",
                "Select one or more passwords first."
            )
            return

        passwords = [
            self.generated_passwords[index]
            for index in selected
        ]

        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(passwords))

        self.status.config(
            text=f"Copied {len(passwords)} password(s)."
        )

    def clear_output(self):

        self.generated_passwords = []
        self.output_listbox.delete(0, tk.END)
        self.last_pool_size = None
        self.passwords_visible = False

        self.visibility_button.config(
            text="Show Passwords"
        )

        self.status.config(text="Output cleared.")

    def show_about(self):

        messagebox.showinfo(
            "About",
            "Password Generator\n"
            "Version 1.5.0\n"
            "Developer: Franz_Hermann1\n\n"
            "Classic Windows desktop application."
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
