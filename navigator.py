# !usr/bin/python3.4

from tkinter import *
from tkinter import filedialog

import meter

class Nav():
    def __init__(self, root):
        self.makeMenu(root)
        toolsFm = Frame(root, bg="#dddddd", height=30)
        toolsFm.pack(side="top", fill="x")

        pane = PanedWindow(root, orient=VERTICAL, sashwidth=6)
        pane.add(self.makeOutputText(pane))
        pane.add(self.makeInputText(pane))
        pane.pack(side="top", expand=YES, fill=BOTH)

        statusFm = Frame(root, bg="#dddddd", height=30)
        statusFm.pack(side="bottom", fill="x")

    def makeMenu(self, root):
        mBar = Menu(root)
        menu_list = (
            {"文件": [{"label": "打开", "cmd": self.test},
                     {"label": "保存", "cmd": self.test},
                     {"label": "另存为", "cmd": self.test},
                     {"label": "退出", "cmd": self.test}
                     ]
             },
            {"设置": [{"label": "电表通信参数", "cmd": self.test},
                     {"label": "台体通信参数", "cmd": self.test}
                     ]
             },
             # 关于命令和脚本的区分：
             # 命令： 指单纯的执行表计的封装命令，如 :get-time
             # 脚本:  指python脚本，表计封装脚本形式为psend(cmd),如psend(":get-time")
             {
             "运行": [{"label": "运行命令", "cmd": self.runCmd},
                     {"label": "运行脚本", "cmd": self.test}
                    ]
             },
            {"帮助": [{"label": "关于", "cmd": self.test},
                     {"label": "帮助", "cmd": self.test}
                     ]
             }
        )
        for index in range(len(menu_list)):
            menuItem = menu_list[index]
            for item in menuItem:
                mfile = Menu(mBar, tearoff=0)
                mBar.add_cascade(menu=mfile, label=item)
                mlist = menuItem[item]
                for i in range(len(mlist)):
                    mfile.add_command(label=mlist[i]["label"],
                                      command=mlist[i]['cmd'])
        root['menu'] = mBar

    def makeInputText(self, root):
        inputFm = Frame(root)
        self.inputText = Text(inputFm, height=10)
        inputScrollbar = Scrollbar(inputFm, orient=VERTICAL)
        self.inputText.pack(side="left", fill=BOTH, expand=YES)
        inputScrollbar.pack(side="left", fill=Y)
        self.inputText.config(yscrollcommand=inputScrollbar.set)
        inputScrollbar.config(command=self.inputText.yview)
        self.inputText.bind('<Control-Shift-B>', self.runCmd)

        # 右键弹出式菜单
        popupCmd = [{"label": "执行命令", "cmd": self.runCmd},
                    {"label": "执行脚本", "cmd": self.runCmd}
                    ]
        self.popup = Menu(root, tearoff=0)
        for item in popupCmd:
            self.popup.add_command(label=item["label"], command=item["cmd"])
        self.inputText.bind('<Button-3>', self.makePopupMenu)

        return inputFm

    def makeOutputText(self, root):
        outputFm = Frame(root)
        self.outputText = Text(outputFm, height=20)
        outputScrollbar = Scrollbar(outputFm, orient=VERTICAL)
        self.outputText.pack(side="left", fill=BOTH, expand=YES)
        outputScrollbar.pack(side="left", fill=Y)
        self.outputText.config(yscrollcommand=outputScrollbar.set)
        outputScrollbar.config(command=self.outputText.yview)
        return outputFm

    def makePopupMenu(self, event):
        self.popup.post(event.x_root, event.y_root)

    def test(self, event):
        print("do testing")

    def runCmd(self, *event):
        """执行表计封装命令,如:get-time

        命令输入区域按Ctrl+Shift+B键按命令方式执行，
        1.首先看是否存在选中区域，如果有则按选中区域命令逐条执行；
        2.如果没有选中区域，则执行光标所在行的命令。
        """
        try:
            commands = self.inputText.get(SEL_FIRST, SEL_LAST).split('\n')
        except TclError:  # 如无选中区域会触发异常
            commands = [self.inputText.get('insert linestart', 'insert lineend')]
        for cmd in commands:
            if len(cmd) > 0:
                meter.runCmd(cmd)

    def write(self, stream):
        self.outputText.insert(END, stream)
        self.outputText.see(END)
        self.outputText.update()

if __name__ == "__main__":
    root = Tk()
    root.title("navigator")
    nav = Nav(root)
    #保存默认stdout,stderr，以便需要的时候返回默认值
    sys.save_out = sys.stdout
    sys.save_err = sys.stderr
    #修改输入输出错误流指向navigator实例，打印信息通过navigator的write函数实现
    sys.stdout = nav
    sys.stderr = nav
    mainloop()
