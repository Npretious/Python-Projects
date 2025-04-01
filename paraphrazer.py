import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime
from transformers import pipeline  # type: ignore
import pyperclip  # type: ignore
from ttkthemes import ThemedTk  # type: ignore
from typing import Optional, List, Dict, Any, Union

class ParaphraseApp:
    def __init__(self, root: ThemedTk) -> None:
        self.root: ThemedTk = root
        self.root.title("Advanced Text Paraphraser")
        self.root.geometry("1200x800")
        
        self.paraphraser: Any = None
        self.input_text: Optional[scrolledtext.ScrolledText] = None
        self.output_text: Optional[scrolledtext.ScrolledText] = None
        self.history_text: Optional[scrolledtext.ScrolledText] = None
        self.status_var = tk.StringVar(value="Ready")
        self.style_var = tk.StringVar(value="Standard")
        self.tone_var = tk.StringVar(value="Neutral")
        self.length_var = tk.StringVar(value="Similar")
        self.word_count_var = tk.StringVar(value="Words: 0")
        self.history: List[Dict[str, Any]] = []
        
        self.configure_styles()
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.create_header(main_frame)
        self.create_content_area(main_frame)
        self.create_bottom_panel(main_frame)
        
        self.status_var.set("Loading T5 model...")
        self.root.update()
        self.paraphraser = pipeline("text2text-generation", model="t5-base")
        self.status_var.set("Ready")

    def configure_styles(self) -> None:
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Helvetica", 12, "italic"))
        style.configure("Status.TLabel", font=("Helvetica", 10, "italic"))
        style.configure("Header.TLabel", font=("Helvetica", 11, "bold"))
        style.configure("Custom.TButton", padding=5)

    def create_header(self, parent: ttk.Frame) -> None:
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Text Paraphraser Pro", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame, 
                                text="Transform your text with advanced paraphrasing techniques",
                                style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0)

    def create_content_area(self, parent: ttk.Frame) -> None:
        input_frame = ttk.LabelFrame(parent, text="Original Text", padding="10")
        input_frame.grid(row=1, column=0, sticky="nsew", padx=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, width=55, height=15, wrap=tk.WORD,
                                                font=("Arial", 11))
        self.input_text.grid(row=0, column=0, pady=5)
        
        self.create_input_buttons(input_frame)  # type: ignore
        
        self.create_control_panel(parent)
        
        output_frame = ttk.LabelFrame(parent, text="Paraphrased Text", padding="10")
        output_frame.grid(row=1, column=1, sticky="nsew", padx=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=55, height=15, wrap=tk.WORD,
                                                font=("Arial", 11))
        self.output_text.grid(row=0, column=0, pady=5)
        
        self.create_output_buttons(output_frame)  # type: ignore

    def create_input_buttons(self, parent: Union[ttk.Frame, ttk.LabelFrame]) -> None:
        input_button_frame = ttk.Frame(parent)
        input_button_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(input_button_frame, text="📂 Load File", 
                command=self.load_file, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(input_button_frame, text="🗑️ Clear Input", 
                command=self.clear_input,
                style="Custom.TButton").grid(row=0, column=1, padx=5)
        
        ttk.Label(input_button_frame, textvariable=self.word_count_var).grid(row=0, column=2, padx=20)
        
        if self.input_text:
            self.input_text.bind('<KeyRelease>', self.update_word_count)

    def create_control_panel(self, parent: ttk.Frame) -> None:
        control_frame = ttk.LabelFrame(parent, text="Paraphrasing Options", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Label(control_frame, text="Style:", style="Header.TLabel").grid(row=0, column=0, padx=5)
        style_combo = ttk.Combobox(control_frame, textvariable=self.style_var,
                                values=["Standard", "Formal", "Casual", "Creative", "Professional", 
                                        "Simple", "Academic"], state="readonly", width=15)
        style_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(control_frame, text="Tone:", style="Header.TLabel").grid(row=0, column=2, padx=5)
        tone_combo = ttk.Combobox(control_frame, textvariable=self.tone_var,
                                values=["Neutral", "Positive", "Negative", "Objective", "Subjective"],
                                state="readonly", width=15)
        tone_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(control_frame, text="Length:", style="Header.TLabel").grid(row=0, column=4, padx=5)
        length_combo = ttk.Combobox(control_frame, textvariable=self.length_var,
                                values=["Shorter", "Similar", "Longer"],
                                state="readonly", width=15)
        length_combo.grid(row=0, column=5, padx=5)
        
        ttk.Button(control_frame, text="✨ Paraphrase", 
                command=self.paraphrase_text,
                style="Custom.TButton").grid(row=0, column=6, padx=20)

    def create_output_buttons(self, parent: Union[ttk.Frame, ttk.LabelFrame]) -> None:
        output_button_frame = ttk.Frame(parent)
        output_button_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(output_button_frame, text="💾 Save to File", 
                command=self.save_file,
                style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(output_button_frame, text="📋 Copy to Clipboard", 
                command=self.copy_to_clipboard,
                style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(output_button_frame, text="🗑️ Clear Output", 
                command=self.clear_output,
                style="Custom.TButton").grid(row=0, column=2, padx=5)

    def create_bottom_panel(self, parent: ttk.Frame) -> None:
        history_frame = ttk.LabelFrame(parent, text="Paraphrasing History", padding="10")
        history_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, width=120, height=6, wrap=tk.WORD,
                                                    font=("Arial", 10))
        self.history_text.grid(row=0, column=0, pady=5)
        
        ttk.Label(parent, textvariable=self.status_var, 
                style="Status.TLabel").grid(row=4, column=0, columnspan=2, sticky="w")

    def paraphrase_text(self) -> None:
        try:
            if not self.input_text or not self.output_text:
                return

            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter some text first!")
                return

            self.status_var.set("Paraphrasing...")
            self.root.update()
            
            style = self.style_var.get().lower()
            tone = self.tone_var.get().lower()
            length = self.length_var.get().lower()
            
            prompt = f"paraphrase: {input_text}"
            
            result = self.paraphraser(prompt, 
                                    max_length=len(input_text) * 2,
                                    min_length=len(input_text) // 2)
            
            paraphrased_text = result[0]['generated_text']
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", paraphrased_text)
            
            self.update_history(style, tone, length)
            self.status_var.set("Paraphrasing complete!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")

    def update_word_count(self, event: Optional[Any] = None) -> None:
        if self.input_text:
            text = self.input_text.get("1.0", tk.END).strip()
            word_count = len(text.split())
            self.word_count_var.set(f"Words: {word_count}")

    def clear_input(self) -> None:
        if self.input_text:
            self.input_text.delete("1.0", tk.END)
            self.update_word_count()

    def clear_output(self) -> None:
        if self.output_text:
            self.output_text.delete("1.0", tk.END)

    def load_file(self) -> None:
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path and self.input_text:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", file.read())
                self.update_word_count()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")

    def save_file(self) -> None:
        if not self.output_text:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.output_text.get("1.0", tk.END))
                self.status_var.set("File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def copy_to_clipboard(self) -> None:
        if not self.output_text:
            return

        text = self.output_text.get("1.0", tk.END).strip()
        pyperclip.copy(text)
        self.status_var.set("Text copied to clipboard!")

    def update_history(self, style: str, tone: str, length: str) -> None:
        if not self.history_text:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"[{timestamp}] Style: {style}, Tone: {tone}, Length: {length}\n"
        self.history_text.insert("1.0", history_entry)

def main() -> None:
    root = ThemedTk(theme="arc")
    app = ParaphraseApp(root)
    root.app = app
    root.mainloop()

if __name__ == "__main__":
    main()