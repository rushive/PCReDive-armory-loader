import tkinter as tk
from tkinter import filedialog
from Loader import Loader


class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('PCReDive-armory-loader')
        self.window.geometry('650x450')
        self.window.resizable(False, False)

        self.path = ''
        self.loader = None
        self.js = ''
        self.res = None

        tk.Label(text='請選擇檔案：', font='KaiTi 14').grid(
            row=0, column=0, padx=(35, 0), pady=(40, 0), sticky=tk.W)
        tk.Label(text='縮放倍率：', font='KaiTi 14').grid(
            row=1, column=0, padx=35, pady=(20, 0), sticky=tk.W)
        tk.Label(text='javascript: ', font='Aria 14').grid(
            row=2, column=0, padx=35, pady=(20, 0), sticky=tk.W)

        self.file_placeholder = tk.Entry(width=25, font='Aria 14')
        self.file_placeholder.grid(row=0, column=1, pady=(40, 0), sticky=tk.W)

        self.scale_content = tk.StringVar(None, '0.5')
        tk.Entry(textvariable=self.scale_content, width=4, font='Aria 14').grid(
            row=1, column=1, pady=(20, 0), sticky=tk.W)

        self.js_content = tk.StringVar()
        tk.Entry(width=25, font='Aria 14', state='readonly', textvariable=self.js_content).grid(
            row=2, column=1, pady=(20, 0), sticky=tk.W)

        tk.Button(text='瀏覽', font='KaiTi 14', command=self.load_file).grid(
            row=0, column=2, padx=(20, 0), pady=(40, 0), sticky=tk.W)

        tk.Button(text='確認', font='KaiTi 14', command=self.confirm).grid(
            row=1, column=2, padx=(20, 0), pady=(20, 0), sticky=tk.W)

        tk.Button(text='複製結果', font='KaiTi 14', command=self.copy).grid(
            row=2, column=2, columnspan=2, padx=(20, 0), pady=(20, 0), sticky=tk.W)

        self.copy_label = tk.Label(text='', font='KaiTi 12', fg='green')
        self.copy_label.grid(row=3, column=2, columnspan=2)

        self.debug_text = tk.Text(width=60, height=10)
        self.debug_text.grid(row=4, column=0, columnspan=3)

    def load_file(self):
        self.path = filedialog.askopenfilename(filetypes=(
            ('mp4 files', '*.mp4'), ('all files', '*.*')))
        self.file_placeholder.delete(0, 'end')
        self.file_placeholder.insert(0, self.path)
        self.debug_text.delete(1.0, tk.END)

    def confirm(self):
        self.loader = Loader(self.path, 0.5 if not self.scale_content.get() else
                             float(self.scale_content.get()), True)
        js, res = self.loader.run()
        for i, v in enumerate(res):
            self.debug_text.insert(tk.END, f'{i}: {v}\n')
        self.js = js
        self.js_content.set(self.js)
        self.debug_text.see(tk.END)
        self.debug_text.insert(tk.END, 'Done !')

    def copy(self):
        self.copy_label['text'] = '已複製'

        self.window.clipboard_clear()
        self.window.clipboard_append(self.js)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.run()
