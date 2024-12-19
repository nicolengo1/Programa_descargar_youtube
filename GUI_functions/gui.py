import tkinter as Tkinter
from tkinter import StringVar


def main():
    # Create the main window
    # def testCallback():



    root = Tkinter.Tk()

    root.title("YouTube Download_functions - 1.0.0")

    root.config(width=500, height=300, background="blue")
    root.minsize(500, 300)


    # Create a label widget
    label = Tkinter.Label(root, text='Pito')
    label.pack()

    var = StringVar()
    textPromp = Tkinter.Entry(width=50,justify="center", textvariable=var)
    textPromp.pack()

    label2 = Tkinter.Label(textvariable=var)
    label2.pack()

    # Start the GUI event loop
    root.mainloop()

# test = textPromp.get()
#
# print(test)
#
# label2.config(text=test)


main()