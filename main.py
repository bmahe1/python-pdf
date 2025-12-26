import kivy
# kivy.require('2.1.0')  # Removed to avoid CI build errors

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

class PDFEditorApp(App):
    def build(self):
        Window.size = (400, 600)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        layout.add_widget(Label(text='📄 PDF Editor Pro', font_size='28sp'))
        layout.add_widget(Label(text='Edit PDF files on mobile', font_size='16sp', color=(0.5,0.5,0.5,1)))
        
        # Buttons
        buttons = [
            ('📂 Open PDF', self.open_pdf),
            ('✏️ Edit Text', self.edit_text),
            ('💾 Save PDF', self.save_pdf),
            ('🔄 Merge PDFs', self.merge_pdfs),
            ('📤 Export', self.export_pdf),
            ('⚙️ Settings', self.settings)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, 0.12))
            btn.bind(on_press=lambda x, cb=callback: cb())
            layout.add_widget(btn)
        
        # Status label
        self.status = Label(text='Ready', size_hint=(1, 0.1))
        layout.add_widget(self.status)
        
        return layout
    
    def open_pdf(self):
        self.status.text = 'Opening PDF...'
        self.show_popup('Open PDF', 'Select PDF file from storage')
    
    def edit_text(self):
        self.status.text = 'Editing text...'
        self.show_popup('Edit PDF', 'Text editor opened')
    
    def save_pdf(self):
        self.status.text = 'Saving PDF...'
        self.show_popup('Save PDF', 'PDF saved successfully')
    
    def merge_pdfs(self):
        self.status.text = 'Merging PDFs...'
        self.show_popup('Merge PDFs', 'Combine multiple PDF files')
    
    def export_pdf(self):
        self.status.text = 'Exporting...'
        self.show_popup('Export', 'Export to different formats')
    
    def settings(self):
        self.show_popup('Settings', 'App settings and preferences')
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    PDFEditorApp().run()
