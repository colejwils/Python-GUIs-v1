# pip install kivy
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.label = Label(text="Hello, World!", font_size=24)
        button = Button(text="Click me!", font_size=24)
        
        button.bind(on_press=self.on_button_press)
        
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        return layout

    def on_button_press(self, instance):
        self.label.text = "Button Pressed!"

if __name__ == '__main__':
    MyApp().run()
