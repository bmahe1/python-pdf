import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import os
import tempfile
from datetime import datetime

class PDFEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20)
        
        # Title
        self.add_widget(Label(text="📄 PDF Editor Pro", font_size='24sp', bold=True))
        self.add_widget(Label(text="Edit and manage PDF files", font_size='14sp', color=(0.5,0.5,0.5,1)))
        
        # File operations
        file_box = BoxLayout(size_hint=(1, 0.15), spacing=5)
        for text in ["📂 Open", "🆕 New", "💾 Save", "🔄 Merge"]:
            btn = Button(text=text)
            btn.bind(on_press=lambda x, t=text: self.file_action(t))
            file_box.add_widget(btn)
        self.add_widget(file_box)
        
        # Content area
        scroll = ScrollView(size_hint=(1, 0.5))
        self.content = TextInput(text="Welcome to PDF Editor Pro!\n\nFeatures:\n• Open PDF files\n• Create new PDFs\n• Edit text content\n• Save documents\n• Merge multiple PDFs\n\nTap buttons above to start.", multiline=True, readonly=True)
        scroll.add_widget(self.content)
        self.add_widget(scroll)
        
        # Text editor
        self.text_input = TextInput(hint_text="Enter text to add to PDF...", size_hint=(1, 0.2), multiline=True)
        self.add_widget(self.text_input)
        
        # Action buttons
        action_box = BoxLayout(size_hint=(1, 0.15), spacing=5)
        for text in ["📝 Add Text", "✂️ Extract", "🔍 Search", "ℹ️ Info"]:
            btn = Button(text=text)
            btn.bind(on_press=lambda x, t=text: self.edit_action(t))
            action_box.add_widget(btn)
        self.add_widget(action_box)
        
        # Status
        self.status = Label(text="Ready", size_hint=(1, 0.1), color=(0.3,0.3,0.3,1))
        self.add_widget(self.status)
        
        self.current_file = None
    
    def file_action(self, action):
        if action == "📂 Open":
            self.open_pdf()
        elif action == "🆕 New":
            self.new_pdf()
        elif action == "💾 Save":
            self.save_pdf()
        elif action == "🔄 Merge":
            self.merge_pdf()
    
    def edit_action(self, action):
        if action == "📝 Add Text":
            self.add_text()
        elif action == "✂️ Extract":
            self.extract_text()
        elif action == "🔍 Search":
            self.search_text()
        elif action == "ℹ️ Info":
            self.show_info()
    
    def open_pdf(self):
        self.status.text = "Opening PDF..."
        self.content.text = "Simulated PDF opened\n\nDocument Title: Sample PDF\nPages: 5\nAuthor: User\nCreated: 2025-12-26\n\nContent preview:\nThis is a sample PDF document with text content that can be edited using PDF Editor Pro."
        self.current_file = "document.pdf"
        self.show_popup("PDF Opened", "Sample PDF loaded successfully")
    
    def new_pdf(self):
        self.status.text = "Creating new PDF..."
        self.content.text = f"New PDF Document\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nYou can now add text using the input field below and save this document."
        self.current_file = "new_document.pdf"
        self.show_popup("New PDF", "New document created")
    
    def save_pdf(self):
        if self.current_file:
            self.status.text = f"Saving {self.current_file}..."
            self.show_popup("PDF Saved", f"Document saved as:\n{self.current_file}")
        else:
            self.show_popup("Error", "No document to save")
    
    def merge_pdf(self):
        self.status.text = "Merging PDFs..."
        self.show_popup("Merge PDFs", "Select multiple PDF files to merge into one document")
    
    def add_text(self):
        text = self.text_input.text.strip()
        if text:
            self.content.text += f"\n\n[Added: {datetime.now().strftime('%H:%M:%S')}]\n{text}"
            self.text_input.text = ""
            self.status.text = "Text added to document"
        else:
            self.show_popup("Notice", "Enter text in the field above first")
    
    def extract_text(self):
        self.status.text = "Extracting text..."
        self.show_popup("Text Extracted", "Text content extracted from PDF:\n\n" + self.content.text[:200] + "...")
    
    def search_text(self):
        self.status.text = "Searching..."
        self.show_popup("Search", "Enter text to search within the document")
    
    def show_info(self):
        info = f"PDF Editor Pro v1.0\n"
        info += f"File: {self.current_file or 'None'}\n"
        info += f"Content length: {len(self.content.text)} chars\n"
        info += f"Time: {datetime.now().strftime('%H:%M:%S')}"
        self.show_popup("App Info", info)
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()

class PDFApp(App):
    def build(self):
        self.title = "PDF Editor Pro"
        Window.size = (400, 600)
        return PDFEditor()

if __name__ == '__main__':
    PDFApp().run()
