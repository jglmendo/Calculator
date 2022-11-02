from cProfile import label
import tkinter as tk

DEFAULT_FONT_STYLE = ("Arial", 20)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
EVAL_DIGIT_FONT_STYLE = ("Arial", 30, "bold")
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
SPECIAL_DIGITS_FONT_STYLE = ("Arial", 19, "bold")

BACKGROUND_LABEL = "#252323"
BLACK_PRESSED = "#23262b"
LIGHT_BLUE = "#235ebb"
LIGHT_GRAY = "#e6e6e6"
OFF_WHITE = "#F8FAFF"
RED = "#910614"
WHITE = "#ffffff"


class Calculator:
    
    def __init__(root):
        root.window = tk.Tk()
        root.window.geometry("375x667")
        root.window.resizable(0,0)
        root.window.minsize(width= 350, height= 550)
        root.window.title("Calculator")
        root.total_expression = ""
        root.current_expression = "" 
        root.display_frame = root.create_display_frame()

        root.total_label, root.label = root.create_display_labels()

        root.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4,2), ".": (4,1)
        }
        
        root.operations = {"/": "\u00F7", "*": "\u00D7", "-": "\u002D", "+": "\u002B"}
        root.buttons_frame = root.create_buttons_frame()
        
        root.buttons_frame.rowconfigure(0, weight=20)
        for x in range(1, 5):
            root.buttons_frame.rowconfigure(x, weight=20)
            root.buttons_frame.columnconfigure(x, weight=20)

        root.create_digit_buttons()
        root.create_operator_buttons()
        root.create_special_buttons()
        root.create_back_space_button()
        root.keyboard_binding()
        
    def keyboard_binding(root):
        root.window.bind("<Return>", lambda event: root.evaluate())
        root.window.bind("=", lambda event: root.evaluate())
        root.window.bind("<BackSpace>", lambda event: root.back_space())
        root.window.bind("<Delete>", lambda event: root.back_space())
        for key in root.digits:
            root.window.bind(str(key), lambda event, digit=key: root.add_to_expression(digit))
        for key in root.operations:
            root.window.bind(key, lambda event, operator=key: root.append_operator(operator))                  

    def create_special_buttons(root):
        root.create_clear_button()
        root.create_back_space_button()
        root.create_eval_button()
        root.create_square_button()
        root.create_squareroot_button()

    def create_display_labels(root):
        total_label = tk.Label(root.display_frame, text = root.total_expression, anchor = tk.E, bg = LIGHT_GRAY, fg = BACKGROUND_LABEL,padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(root.display_frame, text =root.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=BACKGROUND_LABEL,padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_display_frame(root):
        frame = tk.Frame(root.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
        
    def add_to_expression(root, value):
        root.current_expression += str(value)
        root.update_label()

    def create_digit_buttons(root):
        for digit, grid_value in root.digits.items():
            button = tk.Button(root.buttons_frame, text=str(digit), bg=WHITE, fg=BACKGROUND_LABEL, font=DIGITS_FONT_STYLE, borderwidth=4, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, command=lambda x=digit: root.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(root, operator):
        root.current_expression += operator
        root.total_expression += root.current_expression
        root.current_expression = ""
        root.update_total_label()
        root.update_label()

    def create_operator_buttons(root):
        i = 0
        for operator, symbol in root.operations.items():
            button = tk.Button(root.buttons_frame, text=symbol, bg=LIGHT_BLUE, font=DIGITS_FONT_STYLE, borderwidth=4, activeforeground= LIGHT_GRAY, activebackground=BLACK_PRESSED, command = lambda x=operator: root.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1
        
    def clear(root):
        root.current_expression = ""
        root.total_expression = ""
        root.update_label()
        root.update_total_label()

    def create_clear_button(root):
        button = tk.Button(root.buttons_frame, text="C", bg=OFF_WHITE, fg=RED, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, font=DIGITS_FONT_STYLE, borderwidth=4, command=root.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)
    
    def square(root):
        root.current_expression = str(eval(f"{root.current_expression}**2"))
        root.update_label()

    def back_space(root):
        root.current_expression = root.current_expression[:-1]
        root.update_label()

    def create_back_space_button(root):
        button = tk.Button(root.buttons_frame, text="\u232B", bg=OFF_WHITE, fg=RED, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, font=SPECIAL_DIGITS_FONT_STYLE, borderwidth=4, command=root.back_space)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_square_button(root):
        button = tk.Button(root.buttons_frame, text="x²", bg=OFF_WHITE, fg=BACKGROUND_LABEL, font=DEFAULT_FONT_STYLE, borderwidth=4, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, command=root.square)
        button.grid(row=4, column=4, sticky=tk.NSEW)

    def squareroot(root):
        root.current_expression = str(eval(f"{root.current_expression}**0.5"))
        root.update_label()
       
    def create_squareroot_button(root):
        button = tk.Button(root.buttons_frame, text="²\u221ax", bg=OFF_WHITE, fg=BACKGROUND_LABEL, font=SPECIAL_DIGITS_FONT_STYLE, borderwidth=4, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, command=root.squareroot)
        button.grid(row=4, column=3, sticky=tk.NSEW)

    def evaluate(root):
        root.total_expression += root.current_expression
        root.update_total_label()
        try:  
            root.current_expression = str(eval(root.total_expression))
            root.total_expression = ""
        except Exception as e:
            root.current_expression = "Error"
        finally:
            root.update_label()

    def create_eval_button(root):
        button = tk.Button(root.buttons_frame, text="=", bg=OFF_WHITE, fg=BACKGROUND_LABEL, font=EVAL_DIGIT_FONT_STYLE, borderwidth=4, activebackground=BLACK_PRESSED, activeforeground= LIGHT_GRAY, command=root.evaluate)
        button.grid(row=0, column=3, sticky=tk.NSEW)            

    def create_buttons_frame(root):
        frame = tk.Frame(root.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(root):
        expression = root.total_expression
        for operator, symbol in root.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        root.total_label.config(text=expression)

    def update_label(root):
        root.label.config(text=root.current_expression[:12])

    def run(root):
        root.window.mainloop()

Calculator().run()
