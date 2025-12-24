import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

import fitz  # PyMuPDF
import tempfile
from datetime import datetime

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path


class PDFViewer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        if platform == 'android':
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

        # header
        header = BoxLayout(size_hint=(1, 0.1))
        header.add_widget(Label(text="PDF Editor Pro", font_size='24sp', bold=True))
        self.add_widget(header)

        # buttons
        buttons = BoxLayout(size_hint=(1, 0.1), spacing=10)

        buttons.add_widget(Button(text="Open", on_press=self.open_pdf))
        buttons.add_widget(Button(text="Extract", on_press=self.extract_text))
        buttons.add_widget(Button(text="Merge", on_press=self.merge_pdfs))
        buttons.add_widget(Button(text="Split", on_press=self.split_pdf))
        buttons.add_widget(Button(text="Rotate", on_press=self.rotate_pages))
        buttons.add_widget(Button(text="Watermark", on_press=self.add_watermark))

        self.add_widget(buttons)

        # content
        self.pdf_display = Label(text="Open a PDF file to display")
        self.add_widget(self.pdf_display)

        self.current_pdf = None
        self.current_page = 0

    def open_pdf(self, instance):
        chooser = FileChooserListView(filters=["*.pdf"])

        def selected(_, selection, __):
            if selection:
                self.load_pdf(selection[0])
                popup.dismiss()

        chooser.bind(on_submit=selected)

        popup = Popup(title="Select PDF", content=chooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_pdf(self, path):
        try:
            self.current_pdf = fitz.open(path)
            self.current_page = 0
            self.pdf_display.text = f"Opened: {os.path.basename(path)}"
        except Exception as e:
            self.show_error(str(e))

    def extract_text(self, instance):
        if not self.current_pdf:
            self.show_error("No PDF loaded")
            return

        text = self.current_pdf[self.current_page].get_text()
        popup = Popup(title="Extracted Text",
                      content=TextInput(text=text, readonly=True),
                      size_hint=(0.9, 0.9))
        popup.open()

    def split_pdf(self, instance):
        if not self.current_pdf:
            self.show_error("No PDF loaded")
            return

        box = BoxLayout(orientation='vertical')
        input_box = TextInput(hint_text="Enter pages like 1-3,5")

        def do_split(_):
            try:
                pages = []
                for part in input_box.text.split(','):
                    if '-' in part:
                        s, e = map(int, part.split('-'))
                        pages.extend(range(s - 1, e))
                    else:
                        pages.append(int(part) - 1)

                result = fitz.open()
                for p in pages:
                    result.insert_pdf(self.current_pdf, from_page=p, to_page=p)

                output = f"split_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                result.save(output)
                result.close()
                self.show_message(f"Saved: {output}")
            except Exception as e:
                self.show_error(str(e))

        box.add_widget(input_box)
        box.add_widget(Button(text="Split", on_press=do_split))

        popup = Popup(title="Split PDF", content=box, size_hint=(0.8, 0.5))
        popup.open()

    def rotate_pages(self, instance):
        self.show_message("Rotation stub")

    def merge_pdfs(self, instance):
        self.show_message("Merge stub")

    def add_watermark(self, instance):
        self.show_message("Watermark stub")

    def show_error(self, text):
        Popup(title="Error", content=Label(text=text), size_hint=(0.7, 0.3)).open()

    def show_message(self, text):
        Popup(title="Info", content=Label(text=text), size_hint=(0.7, 0.3)).open()


class PDFApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return PDFViewer()


if __name__ == "__main__":
    PDFApp().run()
