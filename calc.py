#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
    
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg='#2b2b2b')
        display_frame.pack(pady=20, padx=20, fill='x')
        
        # Previous calculation display
        self.prev_label = tk.Label(
            display_frame, 
            text="", 
            font=('Arial', 12), 
            bg='#2b2b2b', 
            fg='#888888',
            anchor='e'
        )
        self.prev_label.pack(fill='x', pady=(0, 5))
        
        # Current number display
        self.display = tk.Label(
            display_frame, 
            text="0", 
            font=('Arial', 24, 'bold'), 
            bg='#2b2b2b', 
            fg='white',
            anchor='e',
            relief='sunken',
            bd=2
        )
        self.display.pack(fill='x', ipady=10)
    
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Button configuration
        button_config = {
            'font': ('Arial', 16, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'activebackground': '#555555'
        }
        
        # Define button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['√', '0', '.', '=']
        ]
        
        # Color schemes
        colors = {
            'number': {'bg': '#404040', 'fg': 'white'},
            'operator': {'bg': '#ff9500', 'fg': 'white'},
            'function': {'bg': '#606060', 'fg': 'white'},
            'equals': {'bg': '#ff9500', 'fg': 'white'}
        }
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # Determine button type and color
                if text in '0123456789.':
                    color = colors['number']
                elif text in '+-×÷':
                    color = colors['operator']
                elif text == '=':
                    color = colors['equals']
                else:
                    color = colors['function']
                
                btn = tk.Button(
                    button_frame,
                    text=text,
                    command=lambda t=text: self.button_click(t),
                    **button_config,
                    **color
                )
                
                # Special width for 0 button
                if text == '0':
                    btn.grid(row=i, column=j, columnspan=2, sticky='nsew', padx=2, pady=2)
                else:
                    btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def button_click(self, char):
        if char in '0123456789':
            self.input_number(char)
        elif char == '.':
            self.input_decimal()
        elif char in '+-×÷':
            self.input_operator(char)
        elif char == '=':
            self.calculate()
        elif char == 'C':
            self.clear()
        elif char == '±':
            self.toggle_sign()
        elif char == '%':
            self.percentage()
        elif char == '√':
            self.square_root()
    
    def input_number(self, num):
        if self.should_reset or self.current == "0":
            self.current = num
            self.should_reset = False
        else:
            self.current += num
        self.update_display()
    
    def input_decimal(self):
        if self.should_reset:
            self.current = "0."
            self.should_reset = False
        elif '.' not in self.current:
            self.current += '.'
        self.update_display()
    
    def input_operator(self, op):
        if self.operator and not self.should_reset:
            self.calculate()
        
        self.operator = op
        self.previous = self.current
        self.should_reset = True
        self.update_prev_display()
    
    def calculate(self):
        if not self.operator or not self.previous:
            return
        
        try:
            prev_num = float(self.previous)
            curr_num = float(self.current)
            
            if self.operator == '+':
                result = prev_num + curr_num
            elif self.operator == '-':
                result = prev_num - curr_num
            elif self.operator == '×':
                result = prev_num * curr_num
            elif self.operator == '÷':
                if curr_num == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    return
                result = prev_num / curr_num
            
            # Format result
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))
            
            self.operator = ""
            self.previous = ""
            self.should_reset = True
            self.update_display()
            self.prev_label.config(text="")
            
        except (ValueError, ZeroDivisionError) as e:
            messagebox.showerror("Error", "Invalid calculation!")
            self.clear()
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        self.update_display()
        self.prev_label.config(text="")
    
    def toggle_sign(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
        self.update_display()
    
    def percentage(self):
        try:
            value = float(self.current) / 100
            if value == int(value):
                self.current = str(int(value))
            else:
                self.current = str(value)
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
    
    def square_root(self):
        try:
            value = float(self.current)
            if value < 0:
                messagebox.showerror("Error", "Cannot calculate square root of negative number!")
                return
            result = math.sqrt(value)
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
    
    def update_display(self):
        # Limit display length
        display_text = self.current
        if len(display_text) > 15:
            try:
                # Try to format as scientific notation
                num = float(display_text)
                display_text = f"{num:.6e}"
            except:
                display_text = display_text[:15] + "..."
        
        self.display.config(text=display_text)
    
    def update_prev_display(self):
        if self.previous and self.operator:
            self.prev_label.config(text=f"{self.previous} {self.operator}")
    
    def key_press(self, event):
        key = event.char
        
        # Map keyboard keys to calculator functions
        if key in '0123456789':
            self.button_click(key)
        elif key == '.':
            self.button_click('.')
        elif key == '+':
            self.button_click('+')
        elif key == '-':
            self.button_click('-')
        elif key == '*':
            self.button_click('×')
        elif key == '/':
            self.button_click('÷')
        elif key in '\r\n':  # Enter key
            self.button_click('=')
        elif key in 'cC':
            self.button_click('C')
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear()
    
    def backspace(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()