import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import cv2
import matplotlib.pyplot as plt
import imgProcess
import model


def choose_file():
    """ 选择文件 """
    selectFileName = tk.filedialog.askopenfilename(title='选择文件')
    e.set(selectFileName)


def show_result():
    """ 显示结果 """
    img_path = e.get()
    if len(img_path) == 0:
        tkinter.messagebox.showinfo('提示', '请选择图片路径')
        return

    try:
        img = cv2.imread(img_path)
        test_data = imgProcess.process(img)
        result = model.prediction(test_data)
        plt.imshow(img)
        plt.axis('off')
        plt.title(result, fontsize=20)
        plt.show()
    except:
        tkinter.messagebox.showinfo('提示', '请选择图片路径')


def window():
    """ tk主窗口 """
    root = tk.Tk()

    root.title('手写数字识别')
    root.geometry('500x500')

    root.resizable(False, False)  # 固定窗体大小

    # 文本输入框，用于显示路径
    global e
    e = tk.StringVar()  # 文本输入框
    e_entry = tk.Entry(root, width=20, textvariable=e)
    e_entry.pack()

    # 选择文件按钮
    choose_btn = tk.Button(root, text="选择图片", command=choose_file)
    choose_btn.pack()

    # 预测并展示按钮
    func_btn = tk.Button(root, text="识别并展示结果", command=show_result)
    func_btn.pack()

    root.mainloop()


if __name__ == '__main__':
    window()
