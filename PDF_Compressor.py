from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import PySimpleGUI as sg
import os
import platform
import ctypes

sg.theme('Default1')

def make_dpi_aware():
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
        
make_dpi_aware()

def is_valid_path(filepath):
        if filepath and Path(filepath).exists:
            return True
        sg.popup('Invalid file path.')
        return False 

class CompressPDF:

    def __init__(self, input, output) -> None:
        self.input = input
        self.output = output 

    def compress(self):

        reader = PdfReader(self.input)
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()  # This is CPU intensive!
            writer.add_page(page)

        with open(self.output, "wb") as f:
            writer.write(f)


    def calc_compression(self):
        input_stats = os.stat(self.input)
        output_stats = os.stat(self.output)
        input_mb = (input_stats.st_size / (1024*1024))
        output_mb = (output_stats.st_size / (1024*1024))
        percentage = 100 - ((output_mb * 100) / input_mb)
        difference = input_mb-output_mb
        msg_stats = f"File succesfuly compressed!\nReduction of{difference:.2f} MB ({percentage:.1f}%)"
        sg.popup_no_titlebar(msg_stats, background_color='LavenderBlush3')

class Program:

    def __init__(self) -> None:
        self.layout = [
            [sg.Push(), sg.Text('PDF COMPRESSOR'), sg.Push()],
            [sg.Push(), sg.Text("Select your .pdf file and the output folder,\n and click in the 'compress' button"), sg.Push()],
            [sg.FileBrowse('File', key='-SEARCH_FILE-', file_types=(('PDF files', '*.pdf'),), enable_events=True)],
            [sg.Input(key='input_file')],
            [sg.FolderBrowse('Output folder...', key='-SAVE_PATH-', enable_events=True)],
            [sg.Input(key='output_file')],
            [sg.Push(), sg.Text(''), sg.Push()],
            [sg.Push(), sg.Button('Compress', key='-COMPRESS-'), sg.Push()],
            [sg.Push(), sg.Text(''), sg.Push()],
            [sg.Push(), sg.Text('\u00A9 Fabio Augusto Weck, 2023.'), sg.Push()]
        ]

    def get_layout(self):
        return self.layout
    
program = Program()  
window = sg.Window('Window', program.get_layout())

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-COMPRESS-':
        pdf_file_path = values['input_file']
        output_folder = values['output_file']
        if is_valid_path(pdf_file_path) and is_valid_path(output_folder):
            try:
                compress = CompressPDF(pdf_file_path, output_folder)
                compress.compress()
                compress.calc_compression()
            except:
                sg.popup("Check file path and try again")

    if event == '-SEARCH_FILE-':
        filepath = values['-SEARCH_FILE-'] 
        if is_valid_path(filepath):  
            window['input_file'].update(filepath)

    if event == '-SAVE_PATH-':
        filepath = values['-SEARCH_FILE-']
        if is_valid_path(filepath):
            index_begin = filepath.rindex('/')
            index_end = filepath.rindex('.')
            window['output_file'].update(f"{values['-SAVE_PATH-']}{filepath[index_begin:index_end]}_compressed.pdf")

window.close()