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
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
import os
import tempfile
import json
from datetime import datetime

try:
    from PyPDF2 import PdfReader, PdfWriter
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("PyPDF2 not installed, PDF features limited")

class PDFEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.15))
        title = Label(text="📄 PDF Editor Pro", font_size='28sp', bold=True, color=(0.2, 0.4, 0.8, 1))
        header.add_widget(title)
        self.add_widget(header)
        
        # File Operations
        file_box = BoxLayout(size_hint=(1, 0.15), spacing=10)
        buttons = [
            ("📂 Open PDF", self.open_pdf),
            ("🆕 New PDF", self.new_pdf),
            ("💾 Save PDF", self.save_pdf),
            ("🔄 Merge PDF", self.merge_pdf),
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, size_hint=(0.25, 1))
            btn.background_color = (0.2, 0.6, 1, 1)
            btn.bind(on_press=callback)
            file_box.add_widget(btn)
        
        self.add_widget(file_box)
        
        # PDF Info
        self.info_label = Label(text="No PDF loaded", size_hint=(1, 0.1),
                               halign='left', valign='middle')
        self.info_label.bind(size=self.info_label.setter('text_size'))
        self.add_widget(self.info_label)
        
        # Content Area with Scroll
        scroll = ScrollView(size_hint=(1, 0.4))
        self.content_text = TextInput(
            text="PDF content will appear here...\n\nFeatures:\n• Open and view PDFs\n• Create new PDFs\n• Merge multiple PDFs\n• Save edited PDFs\n• Extract text",
            multiline=True,
            readonly=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        scroll.add_widget(self.content_text)
        self.add_widget(scroll)
        
        # Edit Tools
        tools_box = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        edit_tools = [
            ("📝 Add Text", self.add_text),
            ("✂️ Extract Text", self.extract_text),
            ("🔍 Search", self.search_text),
            ("📊 Info", self.show_info),
        ]
        
        for text, callback in edit_tools:
            btn = Button(text=text, size_hint=(0.25, 1))
            btn.background_color = (0.4, 0.8, 0.4, 1)
            btn.bind(on_press=callback)
            tools_box.add_widget(btn)
        
        self.add_widget(tools_box)
        
        # Status Bar
        self.status_label = Label(text="Ready", size_hint=(1, 0.1),
                                 color=(0.5, 0.5, 0.5, 1))
        self.add_widget(self.status_label)
        
        # Initialize
        self.current_pdf = None
        self.pdf_pages = []
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def open_pdf(self, instance):
        if PDF_SUPPORT:
            self.show_file_chooser("Open PDF", self._load_pdf)
        else:
            self.show_message("Error", "PDF library not installed")
    
    def _load_pdf(self, selection):
        if selection:
            try:
                self.current_pdf = selection[0]
                with open(self.current_pdf, 'rb') as f:
                    reader = PdfReader(f)
                    info = f"PDF Info:\n"
                    info += f"• Pages: {len(reader.pages)}\n"
                    info += f"• Author: {reader.metadata.get('/Author', 'Unknown')}\n"
                    info += f"• Created: {reader.metadata.get('/CreationDate', 'Unknown')}\n"
                    
                    # Extract first page text
                    text = ""
                    if len(reader.pages) > 0:
                        page = reader.pages[0]
                        text = page.extract_text()[:500] + "..." if len(page.extract_text()) > 500 else page.extract_text()
                    
                    self.content_text.text = info + "\nFirst Page Preview:\n" + text
                    self.info_label.text = f"📄 {os.path.basename(self.current_pdf)} - {len(reader.pages)} pages"
                    self.status_label.text = "PDF loaded successfully"
                    
                    # Store pages for editing
                    self.pdf_pages = reader.pages
                    
            except Exception as e:
                self.show_message("Error", f"Could not open PDF: {str(e)}")
        else:
            self.content_text.text = "No PDF selected"
    
    def new_pdf(self, instance):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        
        try:
            c = canvas.Canvas(temp_file.name, pagesize=letter)
            c.drawString(100, 750, "New PDF Document")
            c.drawString(100, 730, f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(100, 710, "This is a new PDF created with PDF Editor Pro")
            c.save()
            
            self.current_pdf = temp_file.name
            self.content_text.text = f"New PDF Created:\n\nFile: {temp_file.name}\nSize: {os.path.getsize(temp_file.name)} bytes\n\nContent:\n• Title: New PDF Document\n• Created with PDF Editor Pro"
            self.info_label.text = "🆕 New Document.pdf"
            self.status_label.text = "New PDF created"
            
        except ImportError:
            # Fallback: Create text file instead
            self.content_text.text = "New PDF Document\n\nCreated with PDF Editor Pro\n\nNote: Install reportlab for full PDF creation"
            self.info_label.text = "📝 New Text Document"
            self.status_label.text = "Created new document (text only)"
    
    def save_pdf(self, instance):
        if not self.current_pdf:
            self.show_message("Error", "No PDF to save")
            return
        
        try:
            if PDF_SUPPORT:
                writer = PdfWriter()
                for page in self.pdf_pages:
                    writer.add_page(page)
                
                with open(self.current_pdf, 'wb') as f:
                    writer.write(f)
                
                self.status_label.text = f"PDF saved: {self.current_pdf}"
                self.show_message("Success", f"PDF saved successfully!\n{self.current_pdf}")
            else:
                # Save as text file
                with open(self.current_pdf, 'w') as f:
                    f.write(self.content_text.text)
                self.status_label.text = "Document saved as text"
                self.show_message("Saved", "Document saved (text format)")
                
        except Exception as e:
            self.show_message("Error", f"Save failed: {str(e)}")
    
    def merge_pdf(self, instance):
        if not PDF_SUPPORT:
            self.show_message("Error", "PDF merge requires PyPDF2")
            return
        
        self.show_message("Info", "Merge feature requires multiple PDF files\n\nIn full version:\n1. Select multiple PDFs\n2. Choose merge order\n3. Save combined PDF")
        self.status_label.text = "Merge feature (premium)"
    
    def add_text(self, instance):
        text = self.show_input_dialog("Add Text", "Enter text to add to PDF:")
        if text:
            self.content_text.text += f"\n\n[Added Text: {datetime.now().strftime('%H:%M:%S')}]\n{text}"
            self.status_label.text = "Text added to document"
    
    def extract_text(self, instance):
        if self.pdf_pages and PDF_SUPPORT:
            all_text = ""
            for i, page in enumerate(self.pdf_pages[:3]):  # First 3 pages only
                text = page.extract_text()
                all_text += f"\n--- Page {i+1} ---\n{text}\n"
            
            self.content_text.text = "Extracted Text:\n" + all_text
            self.status_label.text = f"Text extracted from {len(self.pdf_pages[:3])} pages"
        else:
            self.show_message("Info", "No PDF loaded or PDF library missing")
    
    def search_text(self, instance):
        term = self.show_input_dialog("Search", "Enter search term:")
        if term and term in self.content_text.text:
            self.status_label.text = f"Found '{term}' in document"
        elif term:
            self.status_label.text = f"'{term}' not found"
    
    def show_info(self, instance):
        info = f"PDF Editor Pro v1.0\n"
        info += f"• PDF Support: {'Yes' if PDF_SUPPORT else 'Limited'}\n"
        info += f"• Current File: {self.current_pdf or 'None'}\n"
        info += f"• Pages: {len(self.pdf_pages)}\n"
        info += f"• Time: {datetime.now().strftime('%H:%M:%S')}"
        
        self.show_message("App Info", info)
    
    def show_file_chooser(self, title, callback):
        content = FileChooserListView()
        content.filters = ['*.pdf']
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_selection(chooser, selection):
            popup.dismiss()
            callback(selection)
        
        content.bind(on_submit=lambda instance: on_selection(instance, instance.selection))
        
        # Add cancel button
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(content)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1))
        cancel_btn = Button(text="Cancel", size_hint=(1, 1))
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        layout.add_widget(btn_layout)
        
        popup.content = layout
        popup.open()
    
    def show_message(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, padding=20),
            size_hint=(0.8, 0.5)
        )
        popup.open()
    
    def show_input_dialog(self, title, prompt):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text=prompt)
        text_input = TextInput(multiline=False)
        
        result = [None]  # Use list to store result
        
        def on_ok(instance):
            result[0] = text_input.text
            popup.dismiss()
        
        btn_layout = BoxLayout(size_hint=(1, 0.3))
        ok_btn = Button(text="OK")
        ok_btn.bind(on_press=on_ok)
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(label)
        layout.add_widget(text_input)
        layout.add_widget(btn_layout)
        
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4))
        popup.open()
        
        return result[0]

class PDFApp(App):
    def build(self):
        self.title = "PDF Editor Pro"
        Window.size = (420, 700)
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        return PDFEditor()

if __name__ == '__main__':
    PDFApp().run()
