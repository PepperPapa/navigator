# !usr/bin/python3.4

from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator
from idlelib.textView import view_text
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
import os
import time
import re

import meter
import log
import rs485
import dut

def showNowTime(now, delay):
    while(1):
        now.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(delay)

def psend(cmdin):
    # 简单区分是台体命令还是表计命令，详细的校验在各自模块中完成
    if re.match('^:dut-', cmdin):
        dut.runCmd(cmdin)
    else:
        meter.runCmd(cmdin)

class Nav():
    def __init__(self, root):
        self.root = root
        self.makeMenu(root)
        toolsFm = Frame(root, bg="#dddddd", height=30)
        toolsFm.pack(side="top", fill="x")

        pane = PanedWindow(root, orient=VERTICAL, sashwidth=6)
        pane.add(self.makeOutputText(pane))
        pane.add(self.makeInputText(pane))
        pane.pack(side="top", expand=YES, fill=BOTH)

        statusFm = Frame(root, bg="#dddddd", height=30)
        statusFm.pack(side="bottom", fill="x")

        # 显示输入区域光标的line:column
        self.insertCursorPos = StringVar()
        insertCurLabel = Label(statusFm, textvariable=self.insertCursorPos,
                               fg="gray", bg="#dddddd", width=8)
        insertCurLabel.pack(side="left", fill='y')

        # 实时显示当前系统时间
        self.nowTime = StringVar()
        nowTimeLabel = Label(statusFm, textvariable=self.nowTime,
                             fg="gray", bg="#dddddd", width=18)
        nowTimeLabel.pack(side="right", fill="y")
        self.tTime = Thread(target=showNowTime, args=(self.nowTime, 1))
        self.tTime.setDaemon(True)
        self.tTime.start()

        # 规定同时只能打开一个参数设置窗口，通过该变量进行控制
        self.isComsetDlgOpen = False

    def makeMenu(self, root):
        mBar = Menu(root)
        menu_list = (
            {"文件": [{"label": "打开", "cmd": self.openTestSuite},
                     {"label": "保存", "cmd": self.saveTestSuite},
                     {"label": "另存为", "cmd": self.saveasTestSuite},
                     {"label": "退出", "cmd": self.quit}
                     ]
             },
            {"设置": [{"label": "电表通信参数", "cmd": self.meterComSet},
                     {"label": "台体通信参数",  "cmd": self.dutComSet}
                     ]
             },
             # 关于命令和脚本的区分：
             # 命令： 指单纯的执行表计的封装命令，如 :get-time
             # 脚本:  指python脚本，表计封装脚本形式为psend(cmd),如psend(":get-time")
             {
             "运行": [{"label": "运行命令", "cmd": self.runCmd},
                     {"label": "运行脚本", "cmd": self.runScript}
                    ]
             },
            {"帮助": [{"label": "关于", "cmd": self.pending},
                     {"label": "帮助", "cmd": self.pending}
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
        Percolator(self.inputText).insertfilter(ColorDelegator())
        self.inputText.bind('<Control-Shift-B>', self.runCmd)

        # 右键弹出式菜单
        popupCmd = [{"label": "执行命令", "cmd": self.runCmd},
                    {"label": "执行脚本", "cmd": self.runScript}
                    ]
        self.popup = Menu(root, tearoff=0)
        for item in popupCmd:
            self.popup.add_command(label=item["label"], command=item["cmd"])
        self.inputText.bind('<Button-3>', self.makePopupMenu)

        # 跟踪插入光标的行列信息
        self.inputText.bind('<KeyPress>', self.updateInsertPos)
        self.inputText.bind('<Button-1>', self.updateInsertPos)

        # 读取默认测试脚本
        if os.path.exists(os.getcwd() + "\\testsuite\default.py"):
            f = open(os.getcwd() + "\\testsuite\default.py")
            testsuite = f.read()
            f.close
            self.inputText.insert("1.0", testsuite)

        return inputFm

    def makeOutputText(self, root):
        outputFm = Frame(root)
        self.outputText = Text(outputFm, height=20)
        outputScrollbar = Scrollbar(outputFm, orient=VERTICAL)
        self.outputText.pack(side="left", fill=BOTH, expand=YES)
        outputScrollbar.pack(side="left", fill=Y)
        self.outputText.config(yscrollcommand=outputScrollbar.set)
        outputScrollbar.config(command=self.outputText.yview)

        # 输出结果格式化显示tag设置
        self.outputText.tag_config("err", foreground="red")
        self.outputText.tag_config("ok", foreground="green")

        return outputFm

    def makePopupMenu(self, event):
        self.popup.post(event.x_root, event.y_root)

    def pending(self, *event):
        print("in pending...")

    def updateInsertPos(self, *event):
        self.insertCursorPos.set(':'.join(self.inputText.index(INSERT).split('.')))

    def runCmd(self, *event):
        """执行表计封装命令,如:get-time

        命令输入区域按Ctrl+Shift+B键按命令方式执行，
        1.首先看是否存在选中区域，如果有则按选中区域命令逐条执行；
        2.如果没有选中区域，则执行光标所在行的命令。
        """
        commands = self.inputText.get(SEL_FIRST, SEL_LAST).split('\n')
        # commands长度为1表示并没有选中区域，默认没选中区域测试长度为1
        if (len(commands) <= 1):
            commands = [self.inputText.get('insert linestart', 'insert lineend')]
        for cmd in commands:
            if len(cmd) > 0:
                psend(cmd)

    def runScript(self, *event):
        """运行输入区域脚本

        """
        # 首先尝试执行选中的脚本
        script = self.inputText.get(SEL_FIRST, SEL_LAST)
        # script长度为1表示并没有选中区域，默认没选中区域测试长度为1
        if (len(script) <= 1):
            script = self.inputText.get('1.0', END)
        exec(script)

    def write(self, stream):
        formatTags = []
        if re.search(r'异常|无应答|错误|失败|关闭', stream):
            formatTags.append("err")
        elif re.search(r'成功', stream):
            formatTags.append("ok")

        self.outputText.insert(END, stream, tuple(formatTags))
        self.outputText.see(END)
        self.outputText.update()

        # 记录日志
        # 在有log需要记录前才创建日志记录文件，调用write说明有日志需要记录，
        # 避免没有任何日志也创建日志文件（0kB）
        global isLogCreated
        if isLogCreated == False:
            global log_att
            log_att = log.createLogFile()
            isLogCreated = True
        log.updateLogFile(log_att[0], log_att[1], stream)

    def quit(self):
        self.root.destroy()

    def openTestSuite(self):
        openfilename = filedialog.askopenfilename(
                        initialdir = os.getcwd())
        if len(openfilename) > 0:
            f = open(openfilename)
            try:
                testsuite = f.read()
            finally:
                f.close
            self.inputText.delete("1.0", "end")
            self.inputText.insert("1.0", testsuite)

    def saveTestSuite(self):
        testsuite_dir = os.getcwd() + "\\testsuite"
        testsuite = self.inputText.get("1.0", "end")
        if not os.path.exists(testsuite_dir):
            os.mkdir(testsuite_dir)
        # 内容为空的情况测试实际获取的长度为1，因此大于1的情况表示输入区域有实际内容，
        # 有内容才进行保存
        if len(testsuite) > 1:
            f = open( (testsuite_dir + "\default.py"), 'w')
            f.write(testsuite)
            f.close

    def saveasTestSuite(self):
        saveasfilename = filedialog.asksaveasfilename(initialdir = os.getcwd())
        if len(saveasfilename) > 0:
            testsuite = self.inputText.get("1.0", "end")
            f = open(saveasfilename + ".py", 'w')
            f.write(testsuite)
            f.close

    def meterComSet(self):
        if not self.isComsetDlgOpen:
            ComsetDlg(self, "电表通信参数设置", rs485.mRS)
        self.isComsetDlgOpen = True

    def dutComSet(self):
        if not self.isComsetDlgOpen:
            ComsetDlg(self, "台体通信参数设置", rs485.dRS)
        self.isComsetDlgOpen = True

class ComsetDlg():
    """通信参数设置对话框

    """
    def __init__(self, master, title, rs):
        self.root = Toplevel()
        self.root.resizable(False,False)
        self.root.title(title)
        self.root.geometry('+200+180')
        self.master = master
        self.rs = rs
        self.settings = []

        all_sets = {
            'port': ['COM1', 'COM2', 'COM3', 'COM4', 'COM5'],
            'baudrate': [300, 600, 1200, 2400, 4800, 9600, 19200],
            'bytesize': [5, 6, 7, 8],
            'stopbits': [1, 2],
            'parity': ['O', 'E', 'N'],
            'timeout': ['0.5', '1.5', '2', '2.5']
        }
        cur_set = rs.getParameter()
        para_items = [{"串口:": [all_sets['port'],
                                all_sets['port'].index(cur_set['port'])]},
                    {"波特率:": [all_sets['baudrate'],
                                all_sets['baudrate'].index(cur_set['baudrate'])]},
                    {"数据位:":[all_sets['bytesize'],
                                all_sets['bytesize'].index(cur_set['bytesize'])]},
                    {"停止位:": [all_sets['stopbits'],
                                all_sets['stopbits'].index(cur_set['stopbits'])]},
                    {"校验方式:": [all_sets['parity'],
                                all_sets['parity'].index(cur_set['parity'])]},
                    {"超时时间:": [all_sets['timeout'],
                                all_sets['timeout'].index(str(cur_set['timeout']))]}
                    ]

        item_nums = len(para_items)
        for i in range(item_nums):
            self.root.grid_rowconfigure(i, pad=5)
            for k,v in para_items[i].items():
                lb = Label(self.root, text=k, height=1, width=8)
                lb.grid(row=i, column=0, sticky=NSEW)
                lst = ttk.Combobox(self.root, width=24, values=v[0])
                lst.grid(row=i, column=1, columnspan=3, sticky=NSEW)
                lst.current(v[1])
                self.settings.append(lst)

        self.root.grid_rowconfigure(item_nums, pad=10)
        btn_ok = Button(self.root, text="确定", width=8, height=1,
                        command=self.ok)
        btn_ok.grid(row=item_nums, column=0, columnspan=2)
        btn_cancel = Button(self.root, text="取消", width=8, height=1,
                        command=self.cancel)
        btn_cancel.grid(row=item_nums, column=2, columnspan=2)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)

    def ok(self):
        comPara={}
        comPara['port'] = self.settings[0].get()
        comPara['baudrate'] = int(self.settings[1].get())
        comPara['bytesize'] = int(self.settings[2].get())
        comPara['stopbits'] = float(self.settings[3].get())
        comPara['parity'] = self.settings[4].get()
        comPara['timeout'] = float(self.settings[5].get())
        self.rs.setParameter(comPara)
        self.quit()

    def cancel(self):
        self.quit()

    def quit(self):
        self.master.isComsetDlgOpen = False
        self.root.destroy()

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
    isLogCreated = False

    mainloop()
