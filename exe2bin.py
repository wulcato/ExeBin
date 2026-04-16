import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import base64
import os


class ExeToBinConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Exe to Binary Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.file_path = None
        self.output_mode = tk.StringVar(value="base64")
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame, 
            text="Exe to Binary Converter", 
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(file_frame, text="Selected File:", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        options_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        base64_rb = ttk.Radiobutton(
            options_frame, 
            text="Base64", 
            variable=self.output_mode, 
            value="base64",
            command=self.convert_file
        )
        base64_rb.pack(side=tk.LEFT, padx=(0, 20))
        
        hex_rb = ttk.Radiobutton(
            options_frame, 
            text="Hexadecimal", 
            variable=self.output_mode, 
            value="hex",
            command=self.convert_file
        )
        hex_rb.pack(side=tk.LEFT)
        
        raw_rb = ttk.Radiobutton(
            options_frame, 
            text="Raw Bytes", 
            variable=self.output_mode, 
            value="raw",
            command=self.convert_file
        )
        raw_rb.pack(side=tk.LEFT, padx=(20, 0))
        
        self.format_label = ttk.Label(options_frame, text="Format: BASE64", font=("Helvetica", 9, "italic"))
        self.format_label.pack(side=tk.RIGHT)
        
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.output_text = tk.Text(
            output_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.output_text, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        self.status_label = ttk.Label(main_frame, text="Ready. Select a file to convert.", font=("Helvetica", 9))
        self.status_label.pack(pady=(0, 10))
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        copy_btn = ttk.Button(buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = ttk.Button(buttons_frame, text="Save as File", command=self.save_to_file)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="Clear", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT)
        
        info_label = ttk.Label(
            buttons_frame, 
            text="Python Tkinter Version", 
            font=("Helvetica", 8, "italic"),
            foreground="gray"
        )
        info_label.pack(side=tk.RIGHT)
    
    def browse_file(self):
        file_types = [("Executable files", "*.exe"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~"),
            title="Select an Executable",
            filetypes=file_types
        )
        
        if filename:
            self.file_path = filename
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.convert_file()
    
    def convert_file(self):
        if not self.file_path:
            self.status_label.config(text="Please select a file first!")
            return
        
        try:
            with open(self.file_path, "rb") as f:
                data = f.read()
            
            mode = self.output_mode.get()
            
            if mode == "base64":
                output = base64.b64encode(data).decode("ascii")
                self.format_label.config(text="Format: BASE64")
            elif mode == "hex":
                output = data.hex()
                self.format_label.config(text="Format: HEXADECIMAL")
            else:
                output = " ".join(f"{b:02x}" for b in data)
                self.format_label.config(text="Format: RAW BYTES")
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", output)
            
            file_size = len(data)
            output_len = len(output)
            
            self.status_label.config(
                text=f"Converted: {file_size:,} bytes -> {output_len:,} chars ({mode.upper()})"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert file:\n{str(e)}")
            self.status_label.config(text="Conversion failed!")
    
    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="Copied to clipboard!")
            self.root.after(2000, lambda: self.status_label.config(
                text=f"Converted: {len(content):,} chars" if self.file_path else "Ready."
            ))
        else:
            messagebox.showwarning("Warning", "No content to copy!")
    
    def save_to_file(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to save!")
            return
        
        mode = self.output_mode.get()
        ext = ".b64" if mode == "base64" else ".hex" if mode == "hex" else ".raw"
        
        filename = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(self.file_path) if self.file_path else os.path.expanduser("~"),
            title="Save Output",
            defaultextension=ext,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.file_entry.delete(0, tk.END)
        self.file_path = None
        self.status_label.config(text="Ready. Select a file to convert.")


def main():
    root = tk.Tk()
    app = ExeToBinConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
