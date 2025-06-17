"""
Desktop Timed Typer - Types text at controlled speed into any application
Requires: pip install pyautogui
Note: tkinter comes built-in with Python on Windows

FIXES APPLIED:
- Added debug mode with console output
- Fixed click detection logic
- Added better error handling
- Improved target position selection
- Added failsafe instructions
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import time
import threading

class TimedTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("Timed Typer - Type into Any Application (Debug)")
        self.root.geometry("600x600")
        self.root.configure(bg="#2d2d2d")
        
        self.typing_thread = None
        self.is_typing = False
        self.stop_typing = False
        self.target_position = None
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        
        # Print debug info
        print(f"PyAutoGUI version: {pyautogui.__version__}")
        print(f"Screen size: {pyautogui.size()}")
        print(f"Current mouse position: {pyautogui.position()}")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="⌨️ Timed Typer (Debug)", 
                        font=("Arial", 20, "bold"), 
                        fg='#ffffff', bg='#2d2d2d')
        title.pack(pady=10)
        
        subtitle = tk.Label(self.root, text="Type text at controlled speed into any application", 
                           font=("Arial", 10), 
                           fg='#cccccc', bg='#2d2d2d')
        subtitle.pack(pady=(0, 20))
        
        # Debug toggle
        self.debug_var = tk.BooleanVar(value=True)
        debug_cb = tk.Checkbutton(self.root, text="Debug Mode (console output)", 
                                 variable=self.debug_var,
                                 fg='#cccccc', bg='#2d2d2d',
                                 selectcolor='#404040', activebackground='#2d2d2d',
                                 activeforeground='#ffffff')
        debug_cb.pack()
        
        # Text input
        tk.Label(self.root, text="Text to Type:", font=("Arial", 12, "bold"), 
                fg='#ffffff', bg='#2d2d2d').pack(anchor='w', padx=20)
        
        self.text_area = scrolledtext.ScrolledText(self.root, height=6, 
                                                  font=("Consolas", 11),
                                                  bg='#1e1e1e', fg='#ffffff',
                                                  insertbackground='#ffffff')
        self.text_area.pack(padx=20, pady=(5, 10), fill='both', expand=True)
        
        # Sample text button
        sample_btn = tk.Button(self.root, text="Load Sample Text", 
                              command=self.load_sample_text,
                              bg='#404040', fg='#ffffff', relief='flat')
        sample_btn.pack(pady=(0, 10))
        
        # Test button
        test_btn = tk.Button(self.root, text="Test PyAutoGUI (types 'Hello')", 
                            command=self.test_typing,
                            bg='#28a745', fg='#ffffff', relief='flat')
        test_btn.pack(pady=(0, 10))
        
        # Controls frame
        controls_frame = tk.Frame(self.root, bg='#2d2d2d')
        controls_frame.pack(padx=20, pady=10, fill='x')
        
        # Speed control
        speed_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        speed_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(speed_frame, text="Speed (CPM):", font=("Arial", 10), 
                fg='#ffffff', bg='#2d2d2d').pack(anchor='w')
        
        self.speed_var = tk.StringVar(value="120")  # Slower default for testing
        speed_entry = tk.Entry(speed_frame, textvariable=self.speed_var, width=10,
                              bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
        speed_entry.pack(anchor='w', pady=(2, 0))
        
        # Delay control
        delay_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        delay_frame.pack(side='right', fill='x', expand=True)
        
        tk.Label(delay_frame, text="Delay (seconds):", font=("Arial", 10), 
                fg='#ffffff', bg='#2d2d2d').pack(anchor='e')
        
        self.delay_var = tk.StringVar(value="3")
        delay_entry = tk.Entry(delay_frame, textvariable=self.delay_var, width=10,
                              bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
        delay_entry.pack(anchor='e', pady=(2, 0))
        
        # Preset speeds
        presets_frame = tk.Frame(self.root, bg='#2d2d2d')
        presets_frame.pack(padx=20, pady=5)
        
        tk.Label(presets_frame, text="Quick Speeds:", font=("Arial", 10), 
                fg='#cccccc', bg='#2d2d2d').pack(side='left', padx=(0, 10))
        
        for speed, label in [(30, "Very Slow"), (60, "Slow"), (120, "Medium"), (180, "Normal"), (300, "Fast")]:
            btn = tk.Button(presets_frame, text=f"{label} ({speed})", 
                           command=lambda s=speed: self.speed_var.set(str(s)),
                           bg='#404040', fg='#ffffff', relief='flat',
                           padx=8, pady=2, font=("Arial", 8))
            btn.pack(side='left', padx=2)
        
        # Method selection
        method_frame = tk.Frame(self.root, bg='#2d2d2d')
        method_frame.pack(padx=20, pady=10)
        
        tk.Label(method_frame, text="Target Selection:", font=("Arial", 10, "bold"), 
                fg='#ffffff', bg='#2d2d2d').pack(anchor='w')
        
        self.method_var = tk.StringVar(value="current")
        
        method_options = [
            ("current", "Type at current cursor position"),
            ("click", "Click to select target position (5 sec window)"),
            ("center", "Type at center of screen")
        ]
        
        for value, text in method_options:
            rb = tk.Radiobutton(method_frame, text=text, variable=self.method_var, 
                               value=value, fg='#cccccc', bg='#2d2d2d',
                               selectcolor='#404040', activebackground='#2d2d2d',
                               activeforeground='#ffffff')
            rb.pack(anchor='w', padx=20)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='#2d2d2d')
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="Start Typing", 
                                  command=self.start_typing,
                                  bg='#007acc', fg='#ffffff', 
                                  font=("Arial", 12, "bold"),
                                  padx=20, pady=10, relief='flat')
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Typing", 
                                 command=self.stop_typing_action,
                                 bg='#d73a49', fg='#ffffff',
                                 font=("Arial", 12, "bold"),
                                 padx=20, pady=10, relief='flat',
                                 state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready to type")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               font=("Arial", 10), 
                               fg='#28a745', bg='#2d2d2d')
        status_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="⚠️ FAILSAFE: Move mouse to top-left corner to stop immediately\n" +
                                   "Instructions: 1) Test typing first  2) Enter text  3) Choose target  4) Start",
                               font=("Arial", 9), 
                               fg='#ffc107', bg='#2d2d2d',
                               wraplength=550)
        instructions.pack(pady=10, padx=20)
    
    def debug_print(self, message):
        """Print debug messages if debug mode is enabled"""
        if self.debug_var.get():
            print(f"[DEBUG] {message}")
    
    def test_typing(self):
        """Simple test to verify PyAutoGUI is working"""
        self.debug_print("Starting typing test...")
        
        def test_thread():
            try:
                self.status_var.set("Test: Countdown 3 seconds...")
                for i in range(3, 0, -1):
                    self.status_var.set(f"Test: {i} seconds...")
                    time.sleep(1)
                
                self.status_var.set("Test: Typing 'Hello'...")
                self.debug_print("About to type 'Hello'")
                
                # Type each character with a pause
                for char in "Hello":
                    self.debug_print(f"Typing character: '{char}'")
                    pyautogui.write(char, interval=0.1)
                    time.sleep(0.2)
                
                self.status_var.set("Test completed!")
                self.debug_print("Test completed successfully")
                
            except Exception as e:
                error_msg = f"Test failed: {str(e)}"
                self.status_var.set(error_msg)
                self.debug_print(error_msg)
                print(f"[ERROR] {e}")
        
        thread = threading.Thread(target=test_thread)
        thread.daemon = True
        thread.start()
    
    def load_sample_text(self):
        sample = """Hello World!
This is a test of the timed typer.
Let's see if it works correctly."""
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, sample)
        
    def start_typing(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text to type!")
            return
            
        try:
            speed = int(self.speed_var.get())
            delay = int(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for speed and delay!")
            return
            
        if speed < 1 or speed > 2000:
            messagebox.showerror("Error", "Speed must be between 1 and 2000 CPM!")
            return
            
        if delay < 0 or delay > 60:
            messagebox.showerror("Error", "Delay must be between 0 and 60 seconds!")
            return
            
        self.debug_print(f"Starting typing process: {len(text)} characters at {speed} CPM")
        
        self.is_typing = True
        self.stop_typing = False
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        # Start the typing process
        self.typing_thread = threading.Thread(target=self.typing_process, args=(text, speed, delay))
        self.typing_thread.daemon = True
        self.typing_thread.start()
        
    def typing_process(self, text, speed, delay):
        try:
            self.debug_print("Typing process started")
            
            # Step 1: Countdown
            for i in range(delay, 0, -1):
                if self.stop_typing:
                    return
                self.status_var.set(f"Get ready! Countdown: {i} seconds...")
                self.debug_print(f"Countdown: {i}")
                time.sleep(1)
                
            if self.stop_typing:
                return
                
            # Step 2: Determine target position
            method = self.method_var.get()
            self.debug_print(f"Using method: {method}")
            
            if method == "current":
                # Use current mouse position
                self.target_position = pyautogui.position()
                self.status_var.set("Using current cursor position...")
                self.debug_print(f"Current position: {self.target_position}")
                
            elif method == "center":
                # Use center of screen
                screen_width, screen_height = pyautogui.size()
                self.target_position = (screen_width // 2, screen_height // 2)
                self.status_var.set("Using center of screen...")
                self.debug_print(f"Center position: {self.target_position}")
                
            elif method == "click":
                # Wait for user to click
                self.status_var.set("Click where you want to type! (You have 5 seconds)")
                self.target_position = self.wait_for_click(5)
                
                if self.target_position is None:
                    self.status_var.set("No click detected - operation cancelled")
                    self.debug_print("No click detected")
                    return
                    
            # Step 3: Type the text
            if self.target_position:
                self.type_text(text, speed)
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_var.set(error_msg)
            self.debug_print(error_msg)
            print(f"[ERROR] {e}")
        finally:
            self.cleanup()
    
    def wait_for_click(self, timeout_seconds):
        """Simplified click detection"""
        self.debug_print(f"Waiting for click for {timeout_seconds} seconds")
        
        # Minimize our window
        self.root.withdraw()
        
        try:
            start_time = time.time()
            initial_pos = pyautogui.position()
            self.debug_print(f"Initial position: {initial_pos}")
            
            while time.time() - start_time < timeout_seconds and not self.stop_typing:
                # Just wait and then return current position
                # This is a simplified approach - user should position mouse and wait
                remaining = int(timeout_seconds - (time.time() - start_time))
                if remaining >= 0:
                    self.status_var.set(f"Position mouse and wait! ({remaining}s remaining)")
                
                time.sleep(0.1)
            
            # Return current mouse position
            final_pos = pyautogui.position()
            self.debug_print(f"Selected position: {final_pos}")
            return final_pos
            
        finally:
            self.root.deiconify()  # Show window again
    
    def type_text(self, text, speed):
        if self.stop_typing or self.target_position is None:
            return
            
        self.debug_print(f"Starting to type at position: {self.target_position}")
        
        # Click at target position
        try:
            pyautogui.click(self.target_position[0], self.target_position[1])
            self.debug_print(f"Clicked at {self.target_position}")
            time.sleep(0.5)  # Give more time for the click to register
        except Exception as e:
            error_msg = f"Click error: {str(e)}"
            self.status_var.set(error_msg)
            self.debug_print(error_msg)
            return
        
        # Calculate typing interval
        chars_per_second = speed / 60.0
        interval = 1.0 / chars_per_second if chars_per_second > 0 else 0.1
        self.debug_print(f"Typing interval: {interval:.3f} seconds per character")
        
        self.status_var.set("Typing started...")
        
        # Type character by character
        for i, char in enumerate(text):
            if self.stop_typing:
                self.debug_print("Typing stopped by user")
                break
                
            try:
                if char == '\n':
                    self.debug_print("Typing: ENTER")
                    pyautogui.press('enter')
                elif char == '\t':
                    self.debug_print("Typing: TAB")
                    pyautogui.press('tab')
                else:
                    self.debug_print(f"Typing character: '{char}' (ord: {ord(char)})")
                    pyautogui.write(char, interval=0)
                
                # Update progress
                progress = f"Typing: {i+1}/{len(text)} ({((i+1)/len(text)*100):.1f}%)"
                self.status_var.set(progress)
                
                # Wait between characters
                if i < len(text) - 1:
                    time.sleep(interval)
                    
            except Exception as e:
                error_msg = f"Typing error at character {i} ('{char}'): {str(e)}"
                self.status_var.set(error_msg)
                self.debug_print(error_msg)
                print(f"[ERROR] {e}")
                break
        
        if not self.stop_typing:
            self.status_var.set("Typing completed successfully!")
            self.debug_print("Typing completed successfully")
        else:
            self.status_var.set("Typing stopped by user.")
    
    def stop_typing_action(self):
        self.debug_print("Stop button pressed")
        self.stop_typing = True
        self.cleanup()
        self.status_var.set("Operation stopped.")
    
    def cleanup(self):
        self.debug_print("Cleaning up...")
        self.is_typing = False
        self.target_position = None
        
        # Reset UI on main thread
        self.root.after(0, self.reset_ui)
        
        # Make sure window is visible
        try:
            self.root.deiconify()
        except:
            pass
    
    def reset_ui(self):
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

if __name__ == "__main__":
    print("Starting Timed Typer Debug Version...")
    print("Check console for debug output when 'Debug Mode' is enabled")
    print("=" * 50)
    
    root = tk.Tk()
    app = TimedTyper(root)
    root.mainloop()