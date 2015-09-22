# python3.4
# filename: navWindow.py

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
from encap import *
# import encap
import script

'''新建函数psend的目的是让exec()函数可以直接执行psend命令，
而不需要增加额外的输入，否则要输出encap.psend(cmd)'''
#可以使用 from encap import *来省去下面的函数
#def psend(command):
#    encap.psend(command)

##################GUI应用程序#################################
class navWindow():
    def __init__(self):
        self.logfile_exist = False
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
        self.h_file.add_command(label="关于", command = self.quit)  #command待实现
        self.h_file.add_command(label="帮助", command = self.quit)  #command待实现
        root['menu'] = self.mBar

        #工具栏
        self.toolBar = Frame(root, height=40, relief=GROOVE)
        self.toolBar.grid(row = 0, column = 0, sticky = "ew")
        self.com1_bt = Button(self.toolBar, text="参数1", relief=RAISED, borderwidth = 1, command=meterSettingDlg)
        self.com1_bt.grid(row=0, column=0, sticky='news')
        self.com2_bt = Button(self.toolBar, text="运行", relief=RAISED, borderwidth = 1, command=self.runScript)
        self.com2_bt.grid(row=0, column=1, sticky='news')
        
        #输入输出区域
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
        Percolator(self.in_txt).insertfilter(ColorDelegator()) #输入区域脚本实现语法高亮显示
        self.out_txt.tag_config("alarm", foreground = "red")  #设置tag参数，当出现异常应答帧或无应答时打印红色进行提示
        #读取上一次保存的测试脚本
        self.in_txt.insert(1.0, script.read() )
        
        '''Ctrl+Shift组合键执行当行命令'''
        self.in_txt.bind('<Control-Shift_R>', self.runCommand)  #事件绑定
        self.in_txt.bind('<Button-3>', self.popMenu)  #事件绑定
        
        #状态栏
        self.statusBar = Frame(root, height=22, relief=RAISED, borderwidth = 2)
        self.statusBar.grid(row = 2, column = 0, sticky = "ew")
        self.time_value = StringVar()
        self.time_label = Label(self.statusBar, textvariable=self.time_value, relief=RIDGE)
        self.time_label.pack(side=RIGHT)
        time_value = time.strftime('%Y-%m-%d %H:%M:%S')
        self.timer = threading.Timer(1.0, self.update_time)
        self.timer.start()
        self.time_value.set(time_value)

        #输入区域弹出式菜单,命令输入区域选中要执行的一行或多行命令，右键可以直接执行
        self.popMenu = Menu(root, tearoff=0)
        self.popMenu.add_cascade(label='执行选中命令', command=self.runScript)
    
    def update_time(self):
        time_value = time.strftime('%Y-%m-%d %H:%M:%S')
        self.time_value.set(time_value)
        self.timer = threading.Timer(1.0, self.update_time)
        self.timer.start() 

    #打开指定测试脚本
    def open(self):
        scriptDirDlg(True, self)

    #保存测试脚本
    def save(self):
        contents = self.in_txt.get(1.0, END)
        script.save(contents) 

    #另存脚本
    def saveas(self):
        scriptDirDlg(False, self)

    '''命令输入区域右键会执行选中的脚本，以脚本方式执行'''
    def runScript(self):
        command = self.in_txt.get(SEL_FIRST, SEL_LAST)  #光标选中区域的值
        '''command不为空则执行脚本'''
        if command:
            exec(command)
    
    '''命令输入区域按Ctrl+Shift键按命令方式执行，
    1.首先看是否存在选中区域，如果有则按选中区域命令逐条执行；
    2.如果没有选中区域，则执行光标所在行的命令。
    目前仅实现单行命令执行'''
    def runCommand(self, event):
        '''如果存在选中区域，则顺序执行选中的命令；
        无选中命令区域，则执行当前光标所在行的命令'''
        if self.in_txt.get(SEL_FIRST, SEL_LAST):
            command = self.in_txt.get(SEL_FIRST, SEL_LAST).split('\n')
        else:
            command = [ self.in_txt.get('insert linestart', 'insert lineend') ]
        for i in command:
            cmd_in = encapCmd( i )
            if cmd_in['frame'] != None:    #命令解析没有返回None表示命令解析成功
                output = dl645.sendCmd( dl645.toCOM( cmd_in['frame'] ) ) 
                cmd_out = dl645.toHex(output)
                runinfo = showResult(i, cmd_in, cmd_out)
            else:
                runinfo = cmd_in['sen_fmat'] 

    #弹出式菜单，仅在输入命令区域点击右键有效
    def popMenu(self, event):
        self.popMenu.post(event.x_root, event.y_root)
    
    '''print或报错信息会打印到输出TEXT区域'''
    def write(self, stream):
        if re.match(r'异常应答|无应答', stream):
            self.out_txt.insert(END, stream, "alarm") #异常应答帧或无应答输出信息以红色字体输出已给出明显提示
        else:
            self.out_txt.insert(END, stream )
        self.out_txt.see(END) 
        self.out_txt.update()

        '''记录日志'''
        if self.logfile_exist == False:
            #在有log需要记录前才创建日志记录文件，避免没有任何日志也创建日志文件（0kB）
            global log_att
            log_att = log.createLogFile()  #务必要在mainloop的前面创建，否则不会被执行
            self.logfile_exist = True
        log.updateLogFile(log_att[0], log_att[1], stream)

    def quit(self, event=None):
        self.timer.cancel()  #停止定时器
        self.root.destroy()

class scriptDirDlg():
    '''测试脚本打开对话框'''
    def __init__(self, open_or_saveas, parent):
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
        self.flist.bind('<Double-Button-1>',  self.updateFname)
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
    
    def updateFname(self, event):
        '''鼠标双击事件触发，将listbox中的选中文件名显示到文本框中以作提示'''
        self.fname.delete(0, END)
        self.fname.insert(0, self.flist.get(ACTIVE) )
        
    def open(self):
        fname = self.flist.get(ACTIVE)
        text = script.read(fname)
        #清空脚本输入窗口的脚本
        self.parent.in_txt.delete(1.0, END)
        #显示最新打开的脚本
        self.parent.in_txt.insert(1.0, text)
        self.parent.in_txt.update()
        self.root.destroy()
        
    def save(self):
        #获取输入区域的脚本信息
        text = self.parent.in_txt.get(1.0, END) 
        #读取另存为的文件名
        fname = self.fname.get() + '.txt'
        #以文件名保存脚本
        script.save(text, fname)
        self.root.destroy()

class meterSettingDlg():
    '''电能表参数设置'''
    def __init__(self):
        self.root = root = Toplevel()
        root.title("表计通信参数设置")
        root.resizable(False, False)
        self.frame = Frame(root, borderwidth=5)
        self.frame.pack(expand=YES, fill=BOTH)
        self.comNo = Label(self.frame, text="端口号:")
        self.comNo.grid(row=0, column=0, sticky=W+E)
        self.comValue = Entry(self.frame)
        self.comValue.grid(row=0, column=1, sticky=W+E)
        self.comValue.insert(0, dl645.MeterPara['com'])
        self.baudRate = Label(self.frame, text="波特率:")
        self.baudRate.grid(row=1, column=0, sticky=W+E)
        self.baudRateValue = Entry(self.frame)
        self.baudRateValue.grid(row=1, column=1, sticky=W+E)
        self.baudRateValue.insert(0, str(dl645.MeterPara['baudrate']) )
        self.dataSize = Label(self.frame, text="数据位:")
        self.dataSize.grid(row=2, column=0, sticky=W+E)
        self.dataSizeValue = Entry(self.frame)
        self.dataSizeValue.grid(row=2, column=1, sticky=W+E)
        self.dataSizeValue.insert(0, str(dl645.MeterPara['datasize']) )
        self.stopBits = Label(self.frame, text="停止位:")
        self.stopBits.grid(row=3, column=0, sticky=W+E)
        self.stopBitsValue = Entry(self.frame)
        self.stopBitsValue.grid(row=3, column=1, sticky=W+E)
        self.stopBitsValue.insert(0, str(dl645.MeterPara['stopbits']) )
        self.parity = Label(self.frame, text="校验方式:")
        self.parity.grid(row=4, column=0, sticky=W+E)
        self.parityValue = Entry(self.frame)
        self.parityValue.grid(row=4, column=1, sticky=W+E)
        self.parityValue.insert(0, dl645.MeterPara['parity'])
        self.timeout = Label(self.frame, text="超时时间(s):")
        self.timeout.grid(row=5, column=0, sticky=W+E)
        self.timeoutValue = Entry(self.frame)
        self.timeoutValue.grid(row=5, column=1, sticky=W+E)
        self.timeoutValue.insert(0, str(dl645.MeterPara['timeout']) )
        self.OK = Button(self.frame, text="确定", command=self.modMeterPara)
        self.OK.grid(row=6, column=0, columnspan=2, sticky=W+E)

    def modMeterPara(self):
        dl645.MeterPara['com'] = self.comValue.get()
        dl645.MeterPara['baudrate'] = int( self.baudRateValue.get( ))
        dl645.MeterPara['datasize'] = int( self.dataSizeValue.get() )
        dl645.MeterPara['stopbits'] = int( self.stopBitsValue.get() )
        dl645.MeterPara['parity'] = self.parityValue.get()
        dl645.MeterPara['timeout'] = float( self.timeoutValue.get() )
        self.root.destroy()

 

def main():
    navigator = navWindow()
    '''保存默认stdout,stderr，以便需要的时候返回默认值'''
    #sys.save_in = sys.stdin
    sys.save_out = sys.stdout
    sys.save_err = sys.stderr
    '''修改输入输出错误流指向navigator实例，打印信息通过navigator的write函数实现'''
    sys.stdout = navigator
    sys.stderr = navigator
    navigator.root.mainloop()

if __name__ == '__main__':
    '''日志文件处理:程序首次运行首先创建日志文件，只要输出窗口有新信息就会更新日志文件内容，
    日志文件存放路径，当前目录\log\
    '''
    main()
