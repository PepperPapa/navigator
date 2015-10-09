#!/usr/bin/python3.4
# Filename: navigator_window.py
# Copyright zhongxin2506@outlook.com
# 用户界面及事件处理程序 

from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator
from idlelib.textView import view_text
from tkinter import *
from io import StringIO
import sys
import time
import threading
import re

#自定义module
import log
import dl645
from encap_cmd import *
import script

def psend(command):
    """用psend实现封装命令以脚本方式执行
    
    如过和python脚本一起执行，需要执行表计封装命令，可以使用
    如下方式：
    for i in range(10):
        psend(":get time")
    """
    meter.getCmd(command)
    meter.anyCmd()
    meter.sendCmd()
    meter.getResponse()
    meter.print()
    meter.__init__()

class navWindow(object):
    """主界面
    """
    def __init__(self):
        """主界面的显示

        """
        self.logfile_exist = False #指示是否已经创建日志文件 
        self.root = root = Tk()
        root.title("Navigator")
        root.geometry("800x550")
        root.protocol("WM_DELETE_WINDOW", self.quit)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        #菜单栏
        self.mBar = Menu(root)
        self.m_file = Menu(self.mBar, tearoff=0)
        self.mBar.add_cascade(menu=self.m_file, label='文件')
        self.m_file.add_command(label='打开', command=self.open)
        self.m_file.add_command(label='保存', command=self.save)
        self.m_file.add_command(label='另保存', command=self.saveas)
        self.m_file.add_command(label='退出', command=self.quit)
        self.h_file = Menu(self.mBar, tearoff = 0)
        self.mBar.add_cascade(menu=self.h_file, label='帮助')
        # TODO(self.about): 待实现，暂用self.quit代替以避免出错
        self.h_file.add_command(label="关于", command = self.quit)  
        # TODO(self.help): 待实现，暂用self.quit代替以避免出错
        self.h_file.add_command(label="帮助", command = self.quit)
        root['menu'] = self.mBar
        #工具栏
        self.toolBar = Frame(root, height=40, relief=GROOVE)
        self.toolBar.grid(row = 0, column = 0, sticky = "ew")
        self.com1_bt = Button(self.toolBar, text="参数1", relief=RAISED, \
                                                           borderwidth = 1, command=meterSettingDlg)
        self.com1_bt.grid(row=0, column=0, sticky='news')
        self.com2_bt = Button(self.toolBar, text="运行", relief=RAISED, \
                                                           borderwidth = 1, command=self.runScript)
        self.com2_bt.grid(row=0, column=1, sticky='news')
        #脚本输入text组件、脚本执行输出显示text组件及可拖拽窗口实现
        self.m_fm = Frame(root)
        self.m_fm.grid(row = 1, column = 0, sticky = "news")
        self.pane = PanedWindow(self.m_fm, orient=VERTICAL)
        self.out_fm = Frame(self.pane)
        self.in_fm = Frame(self.pane)
        self.out_txt = Text(self.out_fm, height=25)
        self.out_sbar = Scrollbar(self.out_fm, orient=VERTICAL)
        self.in_txt = Text(self.in_fm, height=10)
        self.in_sbar = Scrollbar(self.in_fm, orient=VERTICAL)
        self.out_txt.pack(side=LEFT, expand=YES, fill=BOTH)
        self.out_sbar.pack(side=LEFT, fill=Y)
        self.out_sbar.config(command=self.out_txt.yview)
        self.out_txt.config(yscrollcommand=self.out_sbar.set)
        self.in_txt.pack(side=LEFT, expand=YES, fill=BOTH)
        self.in_sbar.pack(side=LEFT, fill=Y)
        self.in_sbar.config(command=self.in_txt.yview)
        self.in_txt.config(yscrollcommand=self.in_sbar.set)
        self.pane.add(self.out_fm)
        self.pane.add(self.in_fm)
        self.pane.pack(expand=YES, fill=BOTH)
        #输入区域脚本实现语法高亮显示
        Percolator(self.in_txt).insertfilter(ColorDelegator()) 
        #设置tag参数，当出现异常应答帧或无应答时打印红色进行提示
        self.out_txt.tag_config("alarm", foreground = "red")  
        #程序首次运行即读取上一次保存的测试脚本文件
        self.in_txt.insert(1.0, script.read() )
        #Ctrl+Shift组合键执行电表封装命令，如:get time
        self.in_txt.bind('<Control-Shift_R>', self.runCommand)  
        #右键执行选中脚本
        self.in_txt.bind('<Button-3>', self.popMenu)  
        #输入区域弹出式菜单,命令输入区域选中要执行的一行或多行命令，右键可以直接执行
        self.popMenu = Menu(root, tearoff=0)
        self.popMenu.add_cascade(label='执行选中脚本', command=self.runScript)
        #状态栏，实时显示系统时间
        self.statusBar = Frame(root, height=22, relief=RAISED, borderwidth = 2)
        self.statusBar.grid(row = 2, column = 0, sticky = "ew")
        self.time_value = StringVar()
        self.time_label = Label(self.statusBar, textvariable=self.time_value, relief=RIDGE)
        self.time_label.pack(side=RIGHT)
        time_value = time.strftime('%Y-%m-%d %H:%M:%S')
        self.timer = threading.Timer(1.0, self.update_time)
        self.timer.start()
        self.time_value.set(time_value)
    
    def update_time(self):
        """新建线程，用于更新系统时间

        """
        time_value = time.strftime('%Y-%m-%d %H:%M:%S')
        self.time_value.set(time_value)
        self.timer = threading.Timer(1.0, self.update_time)
        self.timer.start() 

    def open(self):
        """打开菜单命令
        
        """
        scriptDirDlg(True, self)

    def save(self):
        """保存菜单命令

        """
        contents = self.in_txt.get(1.0, END)
        script.save(contents) 

    def saveas(self):
        """另存为菜单命令

        """
        scriptDirDlg(False, self)

    def runScript(self):
        """命令输入区域右键会执行选中的脚本，以脚本方式执行
        
        """
        _script = self.in_txt.get(SEL_FIRST, SEL_LAST)  #光标选中区域的值
        #_script不为空则执行脚本
        if _script:
            exec(_script)
    
    def runCommand(self, event):
        """执行表计封装命令
        
        命令输入区域按Ctrl+Shift键按命令方式执行，
        1.首先看是否存在选中区域，如果有则按选中区域命令逐条执行；
        2.如果没有选中区域，则执行光标所在行的命令。
        """
        if self.in_txt.get(SEL_FIRST, SEL_LAST):
            _command = self.in_txt.get(SEL_FIRST, SEL_LAST).split('\n')
        else:
            _command = [self.in_txt.get('insert linestart', 'insert lineend')]
        for cmd in _command:
            psend(cmd)

    def popMenu(self, event):
        """弹出式菜单，仅在脚本输入text区域内点击右键有效
        
        """
        self.popMenu.post(event.x_root, event.y_root)
    
    def write(self, stream):
        """print或报错信息会打印到输出TEXT区域
        
        """
        if re.search(r'异常应答|无应答|错误', stream):
            #异常应答帧或无应答输出信息以红色字体输出已给出明显提示
            self.out_txt.insert(END, stream, "alarm") 
        else:
            self.out_txt.insert(END, stream )
        self.out_txt.see(END) 
        self.out_txt.update()

        #记录日志
        if self.logfile_exist == False:
            #在有log需要记录前才创建日志记录文件，避免没有任何日志也创建日志文件（0kB）
            global log_att
            log_att = log.createLogFile()  #务必要在mainloop的前面创建，否则不会被执行
            self.logfile_exist = True
        log.updateLogFile(log_att[0], log_att[1], stream)

    def quit(self, event=None):
        """退出主程序

        tip: 程序退出前需要关闭定时器线程，否则python进程一直在运行
        """
        self.timer.cancel()  #停止定时器
        self.root.destroy()

class scriptDirDlg(object):
    """打开、另存为对话框及处理程序

    """
    def __init__(self, open_or_saveas, parent):
        """打开、另存为对话框显示、父窗口为主界面对象

        """
        self.root = root = Toplevel()
        #将主窗口类传到该类中来，以便修改主窗口类的脚本显示
        self.parent = parent
        if open_or_saveas:
            root.title("打开")
        else:
            root.title("另存为")
        root.geometry("450x230")
        root.resizable(False,False)
        self.frm = Frame(root, borderwidth=5)
        self.frm.pack(expand=YES, fill=BOTH)
        self.flist = Listbox(self.frm, width = 60, height = 10)
        self.flist.grid(row = 0, rowspan = 5, column = 0, columnspan = 5, sticky = W+E+N+S)
        self.scroll_bar = Scrollbar(self.frm, orient=VERTICAL)
        self.scroll_bar.grid(row = 0, rowspan = 5, column = 6, sticky = N+S)
        self.scroll_bar.config(command=self.flist.yview)
        self.flist.config(yscrollcommand=self.scroll_bar.set)
        #绑定鼠标双击事件
        self.flist.bind('<Double-Button-1>',  self.updateFileName)
        items = script.openScriptList()
        for i in items:
            self.flist.insert(END, i)
        self.fname = Entry(self.frm, width = 50, relief = GROOVE)
        self.fname.grid(row = 6, column = 0, columnspan = 3, sticky = W+E+N+S)
        if open_or_saveas:
            self.btopen = Button(self.frm, text="打开", width = 10, command=self.open)
            self.btopen.grid(row = 6, column = 4, columnspan = 3, sticky = W+E+N+S)          
        else:
            self.btsave = Button(self.frm, text="保存", width = 10, command=self.save)
            self.btsave.grid(row = 6, column = 4, columnspan = 3, sticky = W+E+N+S)
    
    def updateFileName(self, event):
        """鼠标双击事件触发，将listbox中的选中文件名显示到文本框中以作提示

        """
        self.fname.delete(0, END)
        self.fname.insert(0, self.flist.get(ACTIVE) )
        
    def open(self):
        """打开测试脚本文件到主窗口输入脚本text区域

        """
        fname = self.flist.get(ACTIVE)
        text = script.read(fname)
        #清空脚本输入窗口的脚本
        self.parent.in_txt.delete(1.0, END)
        #显示最新打开的脚本
        self.parent.in_txt.insert(1.0, text)
        self.parent.in_txt.update()
        self.root.destroy()
        
    def save(self):
        """另存测试脚本至硬盘指定目录

        """
        #获取输入区域的脚本信息
        text = self.parent.in_txt.get(1.0, END) 
        #读取另存为的文件名
        fname = self.fname.get() + '.txt'
        #以文件名保存脚本
        script.save(text, fname)
        self.root.destroy()

class meterSettingDlg(object):
    """表计通信参数设置对话框

    """
    def __init__(self):
        """显示对话框

        """
        self.root = root = Toplevel()
        root.title("表计通信参数设置")
        root.resizable(False, False)
        self.frame = Frame(root, borderwidth=5)
        self.frame.pack(expand=YES, fill=BOTH)
        self.comNo = Label(self.frame, text="端口号:")
        self.comNo.grid(row=0, column=0, sticky=W+E)
        self.comValue = Entry(self.frame)
        self.comValue.grid(row=0, column=1, sticky=W+E)
        self.comValue.insert(0, dl645.METER_PARA['com'])
        self.baudRate = Label(self.frame, text="波特率:")
        self.baudRate.grid(row=1, column=0, sticky=W+E)
        self.baudRateValue = Entry(self.frame)
        self.baudRateValue.grid(row=1, column=1, sticky=W+E)
        self.baudRateValue.insert(0, str(dl645.METER_PARA['baudrate']) )
        self.dataSize = Label(self.frame, text="数据位:")
        self.dataSize.grid(row=2, column=0, sticky=W+E)
        self.dataSizeValue = Entry(self.frame)
        self.dataSizeValue.grid(row=2, column=1, sticky=W+E)
        self.dataSizeValue.insert(0, str(dl645.METER_PARA['datasize']) )
        self.stopBits = Label(self.frame, text="停止位:")
        self.stopBits.grid(row=3, column=0, sticky=W+E)
        self.stopBitsValue = Entry(self.frame)
        self.stopBitsValue.grid(row=3, column=1, sticky=W+E)
        self.stopBitsValue.insert(0, str(dl645.METER_PARA['stopbits']) )
        self.parity = Label(self.frame, text="校验方式:")
        self.parity.grid(row=4, column=0, sticky=W+E)
        self.parityValue = Entry(self.frame)
        self.parityValue.grid(row=4, column=1, sticky=W+E)
        self.parityValue.insert(0, dl645.METER_PARA['parity'])
        self.timeout = Label(self.frame, text="超时时间(s):")
        self.timeout.grid(row=5, column=0, sticky=W+E)
        self.timeoutValue = Entry(self.frame)
        self.timeoutValue.grid(row=5, column=1, sticky=W+E)
        self.timeoutValue.insert(0, str(dl645.METER_PARA['timeout']) )
        self.OK = Button(self.frame, text="确定", command=self.modMeterPara)
        self.OK.grid(row=6, column=0, columnspan=2, sticky=W+E)

    def modMeterPara(self):
        """更新表计通信参数

        """
        dl645.METER_PARA['com'] = self.comValue.get()
        dl645.METER_PARA['baudrate'] = int( self.baudRateValue.get( ))
        dl645.METER_PARA['datasize'] = int( self.dataSizeValue.get() )
        dl645.METER_PARA['stopbits'] = int( self.stopBitsValue.get() )
        dl645.METER_PARA['parity'] = self.parityValue.get()
        dl645.METER_PARA['timeout'] = float( self.timeoutValue.get() )
        self.root.destroy()

 

def main():
    """主程序运行前必要的设置

    1.主程序运行前需要把标准输出流、错误流指定到主窗口对象
    以便脚本的执行和错误信息都能在主窗口的输出text区域显示
    2.创建表计封装命令对象
    """
    navigator = navWindow()
    global meter 
    meter = encapCmd()
    #保存默认stdout,stderr，以便需要的时候返回默认值
    #sys.save_in = sys.stdin
    sys.save_out = sys.stdout
    sys.save_err = sys.stderr
    #修改输入输出错误流指向navigator实例，打印信息通过navigator的write函数实现
    sys.stdout = navigator
    sys.stderr = navigator
    navigator.root.mainloop()

if __name__ == '__main__':
    main()

