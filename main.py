import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
import os
import tempfile

class PDFEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.pdf_content = ""
        self.current_file = None
        
        # Title
        self.add_widget(Label(text="PDF Editor App", size_hint=(1, 0.1), font_size='24sp'))
        
        # File selection area
        file_layout = BoxLayout(size_hint=(1, 0.2))
        self.file_btn = Button(text="Select PDF", size_hint=(0.5, 1))
        self.file_btn.bind(on_press=self.select_pdf)
        file_layout.add_widget(self.file_btn)
        
        self.create_btn = Button(text="Create New PDF", size_hint=(0.5, 1))
        self.create_btn.bind(on_press=self.create_new_pdf)
        file_layout.add_widget(self.create_btn)
        
        self.add_widget(file_layout)
        
        # PDF content display
        self.content_label = Label(text="PDF Content will appear here...", 
                                   size_hint=(1, 0.3),
                                   text_size=(Window.width - 20, None))
        self.add_widget(self.content_label)
        
        # Text editor
        edit_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        edit_layout.add_widget(Label(text="Edit PDF Text:", size_hint=(1, 0.1)))
        
        self.text_input = TextInput(multiline=True, 
                                    size_hint=(1, 0.7),
                                    text="Enter text to add to PDF...")
        edit_layout.add_widget(self.text_input)
        
        # Buttons for editing
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        
        self.add_btn = Button(text="Add Text", size_hint=(0.33, 1))
        self.add_btn.bind(on_press=self.add_text_to_pdf)
        btn_layout.add_widget(self.add_btn)
        
        self.clear_btn = Button(text="Clear", size_hint=(0.33, 1))
        self.clear_btn.bind(on_press=self.clear_text)
        btn_layout.add_widget(self.clear_btn)
        
        self.save_btn = Button(text="Save PDF", size_hint=(0.33, 1))
        self.save_btn.bind(on_press=self.save_pdf)
        btn_layout.add_widget(self.save_btn)
        
        edit_layout.add_widget(btn_layout)
        self.add_widget(edit_layout)
        
        # Status bar
        self.status_label = Label(text="Ready", size_hint=(1, 0.1))
        self.add_widget(self.status_label)

    def select_pdf(self, instance):
        # Simulate PDF reading
        self.current_file = "sample.pdf"
        self.pdf_content = "PDF Content:\n1. Introduction to PDF\n2. Chapter One\n3. References"
        self.content_label.text = self.pdf_content
        self.status_label.text = f"Loaded: {self.current_file}"

    def create_new_pdf(self, instance):
        self.current_file = "new_document.pdf"
        self.pdf_content = "New PDF Document\n"
        self.content_label.text = self.pdf_content
        self.status_label.text = "Created new PDF"

    def add_text_to_pdf(self, instance):
        if self.text_input.text:
            self.pdf_content += "\n" + self.text_input.text
            self.content_label.text = self.pdf_content
            self.status_label.text = "Text added to PDF"
            self.text_input.text = ""

    def clear_text(self, instance):
        self.text_input.text = ""
        self.status_label.text = "Text cleared"

    def save_pdf(self, instance):
        if self.current_file:
            # In a real app, this would save to a PDF file
            # For now, simulate saving
            self.status_label.text = f"Saved: {self.current_file}"
            self.show_popup("PDF Saved", f"File saved as {self.current_file}")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()

class PDFApp(App):
    def build(self):
        self.title = "PDF Editor"
        Window.size = (400, 600)
        return PDFEditor()

if __name__ == '__main__':
    PDFApp().run()
