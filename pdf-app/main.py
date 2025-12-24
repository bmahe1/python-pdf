from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import fitz

class PDFEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.text_area = TextInput(size_hint_y=0.8)
        self.add_widget(self.text_area)

        load_btn = Button(text="Load PDF", size_hint_y=0.1)
        load_btn.bind(on_press=self.load_pdf)
        self.add_widget(load_btn)

        save_btn = Button(text="Save Edited PDF", size_hint_y=0.1)
        save_btn.bind(on_press=self.save_pdf)
        self.add_widget(save_btn)

    def load_pdf(self, instance):
        doc = fitz.open("sample.pdf")
        page = doc[0]
        self.text_area.text = page.get_text()

    def save_pdf(self, instance):
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), self.text_area.text)
        doc.save("edited.pdf")

class PDFApp(App):
    def build(self):
        return PDFEditor()

if __name__ == "__main__":
    PDFApp().run()
