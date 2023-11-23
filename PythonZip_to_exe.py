import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
import zipfile
import os
import subprocess
from tkinter import font
from ttkthemes import ThemedStyle 
from tkinter import messagebox
import shutil


def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print(f"File copied from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"Source file not found: {source_path}")
    except PermissionError:
        print(f"Permission error. Make sure you have the necessary permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

class MyApp:
    def __init__(self, root):
        self.root = root
        self.style = ThemedStyle(self.root)
        self.style.theme_use('clam') 
        self.root.title("Executable Generator")
        self.root.geometry("500x300")
        # Define a custom font
        custom_font = font.Font(family="Helvetica",size=16, weight="bold", slant="italic")

        self.zip_file_path = ""
        self.icon_path = ""
        self.exe_location = ""

        self.current_page = 1
        self.create_widgets(custom_font)

    def create_widgets(self, custom_font):
        self.pages = {
            1: self.create_page1,
            2: self.create_page2,
            3: self.create_page3,
            4: self.create_page4,
        }

        self.create_navigation_buttons(custom_font)
        self.show_current_page()

    def create_navigation_buttons(self, custom_font):
        button_style = ttk.Style()
        button_style.configure("TButton", padding=10, relief="flat", font=custom_font, foreground="white", background="green")

        self.back_button = ttk.Button(self.root, text="Back", command=self.go_back, style="TButton")
        self.back_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.next_button = ttk.Button(self.root, text="Next", command=self.go_next, style="TButton")
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def create_page1(self):
        self.destroy_widgets()
        self.page1_label = ttk.Label(self.root, text="Enter Python Code Zip File Path:", font=("Helvetica", 16), foreground="blue")
        self.page1_label.pack(pady=10)

        self.page1_entry = ttk.Entry(self.root, width=40, font=("Helvetica", 16))
        self.page1_entry.pack(pady=10)

        self.page1_button = ttk.Button(self.root, text="Browse", command=self.browse_zip, style="TButton")
        self.page1_button.pack(pady=10)

        self.page1_next_button = ttk.Button(self.root, text="Next", command=self.goto_page2, style="TButton")
        self.page1_next_button.pack(pady=10)

    def create_page2(self):
        self.destroy_widgets()
        self.page2_label1 = ttk.Label(self.root, text="Enter Icon (.ico) File Path:", font=("Helvetica", 16), foreground="blue")
        self.page2_label1.pack(pady=10)

        self.page2_entry1 = ttk.Entry(self.root, width=40, font=("Helvetica", 16))
        self.page2_entry1.pack(pady=10)

        self.page2_button1 = ttk.Button(self.root, text="Browse", command=self.browse_icon, style="TButton")
        self.page2_button1.pack(pady=10)

        self.page2_label2 = ttk.Label(self.root, text="Choose Exe File Location Path:", font=("Helvetica", 16), foreground="blue")
        self.page2_label2.pack(pady=10)

        self.page2_entry2 = ttk.Entry(self.root, width=40, font=("Helvetica", 16))
        self.page2_entry2.pack(pady=10)

        self.page2_button2 = ttk.Button(self.root, text="Browse", command=self.browse_exe_location, style="TButton")
        self.page2_button2.pack(pady=10)

        self.page2_next_button = ttk.Button(self.root, text="Next", command=self.goto_page3, style="TButton")
        self.page2_next_button.pack(pady=10)

        self.page2_back_button = ttk.Button(self.root, text="Back", command=self.go_back, style="TButton")
        self.page2_back_button.pack(pady=10)

    def create_page3(self):
        self.destroy_widgets()
        self.page3_label = ttk.Label(self.root, text="Enter the main Python file (.py) path:", font=("Helvetica", 16), foreground="blue")
        self.page3_label.pack(pady=10)

        self.page3_entry = ttk.Entry(self.root, width=40, font=("Helvetica", 16))
        self.page3_entry.pack(pady=10)

        self.page3_label = ttk.Label(self.root, text="Click the button to convert to .exe file:", font=("Helvetica", 16), foreground="blue")
        self.page3_label.pack(pady=10)

        self.page3_button = ttk.Button(self.root, text="Convert to .exe file", command=self.run_conversion, style="TButton")
        self.page3_button.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)

        self.page3_next_button = ttk.Button(self.root, text="Next", command=self.goto_page4, style="TButton")
        self.page3_next_button.pack(pady=10)

        self.page3_back_button = ttk.Button(self.root, text="Back", command=self.go_back, style="TButton")
        self.page3_back_button.pack(pady=10)

    def create_page4(self):
        self.destroy_widgets()
        self.page4_label = ttk.Label(self.root, text="You have reached the final page!", font=("Helvetica", 16), foreground="blue")
        self.page4_label.pack(pady=10)

        self.page4_button = ttk.Button(self.root, text="Finish", command=self.root.destroy, style="TButton")
        self.page4_button.pack(pady=10)

    def show_current_page(self):
        self.pages[self.current_page]()

    def destroy_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def go_back(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.show_current_page()

    def go_next(self):
        if self.current_page < 4:
            self.current_page += 1
            self.show_current_page()

    def browse_zip(self):
        file_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if file_path:
            self.page1_entry.delete(0, tk.END)
            self.page1_entry.insert(0, file_path)

    def browse_icon(self):
        file_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if file_path:
            self.page2_entry1.delete(0, tk.END)
            self.page2_entry1.insert(0, file_path)

    def browse_exe_location(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.page2_entry2.delete(0, tk.END)
            self.page2_entry2.insert(0, folder_path)

    def run_conversion(self):
        self.progress_var.set(0)

        def run_conversion_thread():
            main_py_path = self.page3_entry.get()  
            zip_file_name, _ = os.path.splitext(os.path.basename(self.zip_file_path))
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('temp')
            exist_path = os.path.join('temp',zip_file_name,main_py_path)
            if not os.path.exists(exist_path):
                messagebox.showerror("Error", "Invalid main Python file path.")
                return

            main_frame_path = os.path.join('temp', zip_file_name, main_py_path)
            pyinstaller_cmd = f'pyinstaller  --icon="{self.icon_path}" --onefile {main_frame_path}'
            subprocess.run(pyinstaller_cmd, shell=True)

            self.progress_var.set(100)
            main_py_path=main_py_path.replace('.py', '.exe')
            main_frame_path = os.path.join('dist',main_py_path)
            copy_file(main_frame_path,self.exe_location)
            shutil.rmtree('dist')
            shutil.rmtree('build')
            shutil.rmtree('temp')
        conversion_thread = Thread(target=run_conversion_thread)
        conversion_thread.start()

    def goto_page2(self):
        self.zip_file_path = self.page1_entry.get()
        if self.page1_entry.get() == "":
            messagebox.showerror("Error", "Please select the Python Code Zip File.")
            return
        else :
            self.icon_path = ""
            self.exe_location = ""
            self.current_page = 2
            self.show_current_page()

    def goto_page3(self):
        if self.page2_entry1.get() == "" or self.page2_entry2.get() == "":
                messagebox.showerror("Error", "Please select both the Icon File and Exe File Location.")
                return
        else :
            self.icon_path = self.page2_entry1.get()
            self.exe_location = self.page2_entry2.get()
            self.current_page = 3
            self.show_current_page()

    def goto_page4(self):
        self.current_page = 4
        self.show_current_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
