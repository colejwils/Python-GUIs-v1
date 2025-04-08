# pip install flet
import flet as ft

def main(page: ft.Page):
    page.title = "Hello Flet!"
    # Center align contents vertically and horizontally
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Create a Text widget
    txt = ft.Text(value="Hello, World!", size=30)

    # Define a button click callback
    def button_click(e):
        txt.value = "Button Pressed!"
        page.update()  # Refresh the page to show updated text

    # Create a button widget
    button = ft.ElevatedButton(text="Click me!", on_click=button_click)

    # Add the text and button widgets to the page
    page.add(txt, button)

# Start the Flet app
ft.app(target=main)
