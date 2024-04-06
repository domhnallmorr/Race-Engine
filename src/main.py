import customtkinter

from race_engine_controller import race_engine_controller

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("Race Engine V0.0.7")
controller = race_engine_controller.RaceEngineController(app)

app.after(0, lambda:app.state("zoomed"))
app.mainloop()

