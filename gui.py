import tkinter as tk
from tkinter import filedialog
from Loader import Loader

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('PCReDive-armory-loader')
        self.window.geometry('650x300')
        self.window.resizable(False, False)

        self.path = ''
        self.loader = None
        self.ret = ''

        self.file_label = tk.Label(text='請選擇檔案：', font='KaiTi 18')
        self.file_label.place(x=30, y=60)

        self.file_placeholder = tk.Entry(width=35, font='KaiTi 14')
        self.file_placeholder.place(x=170, y=65)

        self.js_label = tk.Label(text='javascript: ', font='Aria 15')
        self.js_label.place(x=45, y=120)

        self.file_btn = tk.Button(text='瀏覽', font='KaiTi 15', command=self.load_file)
        self.file_btn.place(x=550, y=60)

        self.js_placeholder = tk.Entry(width=27, font='Aria 15')
        self.js_placeholder.place(x=170, y=120)

        self.confirm_btn = tk.Button(text='確認', font='KaiTi 15', command=self.confirm)
        self.confirm_btn.place(x=150, y=200)

        self.confirm_label = tk.Label(text='', font='KaiTi 12', fg='red')
        self.confirm_label.place(x=160, y=250)

        self.copy_btn = tk.Button(text='複製結果', font='KaiTi 15', command=self.copy)
        self.copy_btn.place(x=350, y=200)

        self.copy_label = tk.Label(text='', font='KaiTi 12', fg='green')
        self.copy_label.place(x=380, y=250)

    def load_file(self):
        self.path = filedialog.askopenfilename(filetypes=(('mp4 files', '*.mp4'), ('all files', '*.*')))
        self.file_placeholder.delete(0, 'end')
        self.file_placeholder.insert(0, self.path)

    def confirm(self):
        self.confirm_label['text'] = '處理中'

        self.loader = Loader(self.path, 0.5, True)
        self.ret = self.loader.run()
        self.js_placeholder.delete(0, 'end')
        self.js_placeholder.insert(0, self.ret)
        self.confirm_label['fg'] = 'blue'
        self.confirm_label['text'] = '已完成'

    def copy(self):
        self.copy_label['text'] = '已複製'

        self.window.clipboard_clear()
        self.window.clipboard_append(self.ret)

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
