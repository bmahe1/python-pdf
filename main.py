import os
import sys
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
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
import fitz  # PyMuPDF
from PIL import Image as PILImage
import io
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
        
        # Request permissions on Android
        if platform == 'android':
            request_permissions([Permission.READ_EXTERNAL_STORAGE, 
                                Permission.WRITE_EXTERNAL_STORAGE])
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1))
        self.title_label = Label(text='PDF Editor Pro', font_size='24sp', bold=True)
        header.add_widget(self.title_label)
        self.add_widget(header)
        
        # Button Panel
        button_panel = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.open_btn = Button(text='Open PDF', on_press=self.open_pdf)
        self.extract_btn = Button(text='Extract Text', on_press=self.extract_text)
        self.merge_btn = Button(text='Merge PDFs', on_press=self.merge_pdfs)
        self.split_btn = Button(text='Split PDF', on_press=self.split_pdf)
        self.rotate_btn = Button(text='Rotate', on_press=self.rotate_pages)
        self.watermark_btn = Button(text='Watermark', on_press=self.add_watermark)
        
        button_panel.add_widget(self.open_btn)
        button_panel.add_widget(self.extract_btn)
        button_panel.add_widget(self.merge_btn)
        button_panel.add_widget(self.split_btn)
        button_panel.add_widget(self.rotate_btn)
        button_panel.add_widget(self.watermark_btn)
        
        self.add_widget(button_panel)
        
        # PDF Content Area
        content_area = BoxLayout(size_hint=(1, 0.8))
        
        # Left panel for thumbnails
        self.thumbnail_panel = ScrollView(size_hint=(0.3, 1))
        self.thumbnail_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.thumbnail_grid.bind(minimum_height=self.thumbnail_grid.setter('height'))
        self.thumbnail_panel.add_widget(self.thumbnail_grid)
        content_area.add_widget(self.thumbnail_panel)
        
        # Right panel for PDF content
        right_panel = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        
        # Page navigation
        nav_panel = BoxLayout(size_hint=(1, 0.1))
        self.prev_btn = Button(text='< Prev', on_press=self.prev_page)
        self.page_label = Label(text='Page: 1/1')
        self.next_btn = Button(text='Next >', on_press=self.next_page)
        nav_panel.add_widget(self.prev_btn)
        nav_panel.add_widget(self.page_label)
        nav_panel.add_widget(self.next_btn)
        right_panel.add_widget(nav_panel)
        
        # PDF display
        self.pdf_display = ScrollView(size_hint=(1, 0.9))
        self.pdf_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.pdf_content.bind(minimum_height=self.pdf_content.setter('height'))
        self.pdf_display.add_widget(self.pdf_content)
        right_panel.add_widget(self.pdf_display)
        
        content_area.add_widget(right_panel)
        self.add_widget(content_area)
        
        # Status bar
        self.status_label = Label(text='Ready', size_hint=(1, 0.05))
        self.add_widget(self.status_label)
        
        # PDF document variables
        self.current_pdf = None
        self.current_page = 0
        self.total_pages = 0
        self.pdf_path = None
        
    def open_pdf(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(filters=['*.pdf'])
        
        def load_pdf(instance, selection, touch):
            if selection:
                self.load_pdf_file(selection[0])
                popup.dismiss()
        
        filechooser.bind(on_submit=load_pdf)
        
        content.add_widget(filechooser)
        
        popup = Popup(title='Select PDF File', 
                     content=content, 
                     size_hint=(0.9, 0.9))
        popup.open()
    
    def load_pdf_file(self, path):
        try:
            self.pdf_path = path
            self.current_pdf = fitz.open(path)
            self.total_pages = len(self.current_pdf)
            self.current_page = 0
            self.update_display()
            self.update_thumbnails()
            self.status_label.text = f'Loaded: {os.path.basename(path)}'
        except Exception as e:
            self.show_error(f'Error loading PDF: {str(e)}')
    
    def update_display(self):
        self.pdf_content.clear_widgets()
        
        if self.current_pdf and self.total_pages > 0:
            page = self.current_pdf[self.current_page]
            
            # Get page as image
            mat = fitz.Matrix(2, 2)  # Zoom factor
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to bytes for Kivy Image
            img_data = pix.tobytes("png")
            
            # Save to temp file and display
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp.write(img_data)
                tmp_path = tmp.name
            
            # Display image
            img = Image(source=tmp_path, size_hint=(None, None))
            img.size = (pix.width / 4, pix.height / 4)  # Scale down for display
            self.pdf_content.add_widget(img)
            
            # Update page label
            self.page_label.text = f'Page: {self.current_page + 1}/{self.total_pages}'
            
            # Clean up temp file
            Clock.schedule_once(lambda dt: os.unlink(tmp_path), 1)
    
    def update_thumbnails(self):
        self.thumbnail_grid.clear_widgets()
        
        if self.current_pdf:
            for i in range(min(10, self.total_pages)):  # Show first 10 thumbnails
                page = self.current_pdf[i]
                mat = fitz.Matrix(0.5, 0.5)  # Small thumbnails
                pix = page.get_pixmap(matrix=mat)
                
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    tmp.write(pix.tobytes("png"))
                    tmp_path = tmp.name
                
                btn = Button(text=f'Page {i+1}', 
                           size_hint_y=None, 
                           height=60,
                           on_press=lambda instance, idx=i: self.go_to_page(idx))
                self.thumbnail_grid.add_widget(btn)
    
    def go_to_page(self, page_idx):
        self.current_page = page_idx
        self.update_display()
    
    def prev_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()
    
    def next_page(self, instance):
        if self.current_pdf and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_display()
    
    def extract_text(self, instance):
        if not self.current_pdf:
            self.show_error('No PDF loaded')
            return
        
        content = BoxLayout(orientation='vertical', size=(400, 600))
        text_input = TextInput(text='', size_hint=(1, 0.9))
        
        # Extract text from current page
        page = self.current_pdf[self.current_page]
        text = page.get_text()
        
        text_input.text = text if text else 'No text found on this page'
        
        content.add_widget(text_input)
        
        popup = Popup(title='Extracted Text', 
                     content=content,
                     size_hint=(0.8, 0.8))
        popup.open()
    
    def merge_pdfs(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(filters=['*.pdf'], multiselect=True)
        
        def merge_selected(instance, selection, touch):
            if len(selection) > 1:
                try:
                    result = fitz.open()
                    for pdf_path in selection:
                        pdf = fitz.open(pdf_path)
                        result.insert_pdf(pdf)
                        pdf.close()
                    
                    # Save merged PDF
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f'merged_{timestamp}.pdf'
                    
                    if platform == 'android':
                        storage_path = primary_external_storage_path()
                        output_path = os.path.join(storage_path, 'Documents', output_path)
                    
                    result.save(output_path)
                    result.close()
                    
                    self.show_message(f'PDFs merged successfully!\nSaved to: {output_path}')
                    popup.dismiss()
                except Exception as e:
                    self.show_error(f'Error merging PDFs: {str(e)}')
        
        filechooser.bind(on_submit=merge_selected)
        content.add_widget(filechooser)
        
        popup = Popup(title='Select PDFs to Merge (2 or more)', 
                     content=content,
                     size_hint=(0.9, 0.9))
        popup.open()
    
    def split_pdf(self, instance):
        if not self.current_pdf:
            self.show_error('No PDF loaded')
            return
        
        content = BoxLayout(orientation='vertical')
        text_input = TextInput(hint_text='Enter page numbers to extract (e.g., 1-3,5,7-9)')
        
        def perform_split(instance):
            try:
                pages_text = text_input.text
                # Parse page ranges
                pages = []
                for part in pages_text.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages.extend(range(start-1, end))
                    else:
                        pages.append(int(part)-1
                
                # Create new PDF with selected pages
                result = fitz.open()
                for page_num in pages:
                    if 0 <= page_num < self.total_pages:
                        result.insert_pdf(self.current_pdf, from_page=page_num, to_page=page_num)
                
                # Save split PDF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f'split_{timestamp}.pdf'
                
                if platform == 'android':
                    storage_path = primary_external_storage_path()
                    output_path = os.path.join(storage_path, 'Documents', output_path)
                
                result.save(output_path)
                result.close()
                
                self.show_message(f'PDF split successfully!\nSaved to: {output_path}')
                popup.dismiss()
            except Exception as e:
                self.show_error(f'Error splitting PDF: {str(e)}')
        
        split_btn = Button(text='Split PDF', on_press=perform_split)
        content.add_widget(Label(text='Enter page ranges to extract:'))
        content.add_widget(text_input)
        content.add_widget(split_btn)
        
        popup = Popup(title='Split PDF', 
                     content=content,
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def rotate_pages(self, instance):
        if not self.current_pdf:
            self.show_error('No PDF loaded')
            return
        
        content = BoxLayout(orientation='vertical')
        
        def rotate_all(angle):
            try:
                for page_num in range(self.total_pages):
                    page = self.current_pdf[page_num]
                    page.set_rotation(angle)
                
                # Save rotated PDF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f'rotated_{timestamp}.pdf'
                
                if platform == 'android':
                    storage_path = primary_external_storage_path()
                    output_path = os.path.join(storage_path, 'Documents', output_path)
                
                self.current_pdf.save(output_path)
                self.show_message(f'PDF rotated successfully!\nSaved to: {output_path}')
                popup.dismiss()
                self.load_pdf_file(output_path)  # Reload the rotated PDF
            except Exception as e:
                self.show_error(f'Error rotating PDF: {str(e)}')
        
        btn_90 = Button(text='Rotate 90°', on_press=lambda x: rotate_all(90))
        btn_180 = Button(text='Rotate 180°', on_press=lambda x: rotate_all(180))
        btn_270 = Button(text='Rotate 270°', on_press=lambda x: rotate_all(270))
        
        content.add_widget(Label(text='Rotate all pages:'))
        content.add_widget(btn_90)
        content.add_widget(btn_180)
        content.add_widget(btn_270)
        
        popup = Popup(title='Rotate PDF', 
                     content=content,
                     size_hint=(0.6, 0.4))
        popup.open()
    
    def add_watermark(self, instance):
        if not self.current_pdf:
            self.show_error('No PDF loaded')
            return
        
        content = BoxLayout(orientation='vertical')
        text_input = TextInput(hint_text='Enter watermark text')
        
        def apply_watermark(instance):
            try:
                watermark_text = text_input.text
                if not watermark_text:
                    watermark_text = "CONFIDENTIAL"
                
                # Create watermarked copy
                result = fitz.open()
                result.insert_pdf(self.current_pdf)
                
                for page_num in range(len(result)):
                    page = result[page_num]
                    # Add watermark to each page
                    page.insert_text((page.rect.width/2, page.rect.height/2), 
                                    watermark_text, 
                                    fontsize=50, 
                                    rotate=45, 
                                    color=(0.5, 0.5, 0.5, 0.3))
                
                # Save watermarked PDF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f'watermarked_{timestamp}.pdf'
                
                if platform == 'android':
                    storage_path = primary_external_storage_path()
                    output_path = os.path.join(storage_path, 'Documents', output_path)
                
                result.save(output_path)
                result.close()
                
                self.show_message(f'Watermark added successfully!\nSaved to: {output_path}')
                popup.dismiss()
                self.load_pdf_file(output_path)  # Reload watermarked PDF
            except Exception as e:
                self.show_error(f'Error adding watermark: {str(e)}')
        
        apply_btn = Button(text='Apply Watermark', on_press=apply_watermark)
        content.add_widget(Label(text='Enter watermark text:'))
        content.add_widget(text_input)
        content.add_widget(apply_btn)
        
        popup = Popup(title='Add Watermark', 
                     content=content,
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def show_error(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        
        popup = Popup(title='Error', 
                     content=content,
                     size_hint=(0.6, 0.3))
        popup.open()
    
    def show_message(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        
        popup = Popup(title='Success', 
                     content=content,
                     size_hint=(0.7, 0.4))
        popup.open()

class PDFApp(App):
    def build(self):
        self.title = 'PDF Editor Pro'
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        return PDFViewer()

if __name__ == '__main__':
    PDFApp().run()
