
import sys
from tkinter import Tk
from gpa_app import GPAApp

if __name__ == "__main__":
    root = Tk()
    app = GPAApp(root)
    root.mainloop()
    sys.exit(0)
