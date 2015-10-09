#!/usr/bin/python3.4
# encap.py
# 处理电表通信命令的封装及回显格式处理

import math
import time
import re
import dl645
import navigator_window
import log

#全局变量
ADDRESS = ["11","11","11","11","11","11"] #通信地址

def encapCmd(command):
    '''把电能表的通信命令封装成有明确含义的英文命令形式，并返回该命令返回帧解析所需要的关键信息
    帧格式：68+通信地址+68+控制码+数据长度+数据域+校验和+16
    命令格式：   
    :get XXX XXX  查询命令  第一个参数表示查询命令的含义，第二个参数表示需要附加的参数
    '''
    #读取时间  :get time    
    if re.match(r':get time', command):
        address = ADDRESS
        code = ["11"]
        length = ["04"]
        data = ["02","01","00","04"]  #数据标识已按从高到底处理
        tem = ['68']+address+['68']+code+length+dl645.add33H(data)
        crc = dl645.getCheckSum( tem )
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+校验和+16
        frame = tem + [crc] + ['16']
        return dict(
			frame = frame,
            cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
            sen_fmat = "",
            rec_fmat = "抄读时间为 {0[12]}{0[13]}:{0[10]}{0[11]}:{0[8]}{0[9]}"
		)
    
    #设定时间  :set time hhmmss
    if re.match(r':set time ', command):
        data_id =  ["02","01","00","04"]
        password = ["04","11","11","11"]
        operator = ["01","00","00","00"]
        tem = command.split()[2] #提取时间参数
        #####################这段代码有问题，当用户输入参数长度不足时会报错
        set_time = [ tem[4:6], tem[2:4], tem[0:2] ]
        address = ADDRESS
        code = ["14"]
        length = ["0F"]
        tem1 = ['68']+address+['68']+code+length+dl645.add33H(data_id+password+operator+set_time)
        crc = dl645.getCheckSum(tem1)
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+密码+操作者代码+时间参数+校验和+16
        frame = tem1 + [crc] + ['16']
        return dict(
            frame = frame,
            cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data_id[::-1] ) ),
            sen_fmat = "写时间参数为 " + "{0}:{1}:{2}".format( set_time[2], set_time[1], set_time[0] ),
            rec_fmat = ""
        )
    
    #读取通信地址  :get address
    if re.match(r':get address', command):
        return dict(
            frame = "68 AA AA AA AA AA AA 68 13 00 DF 16".split(),
            cmd_info = command,
            sen_fmat = "",
            rec_fmat = "抄读通信地址为 {0[10]}{0[11]} {0[8]}{0[9]} {0[6]}{0[7]} {0[4]}{0[5]} {0[2]}{0[3]} {0[0]}{0[1]}" 
        )
    
    #写通信地址   :set address xxxxxxxxxxxx
    if re.match(r':set address ', command):
        tem = command.split()[2]
        #####################这段代码有问题，当用户输入参数长度不足时会报错
        set_addr = [ tem[10:12],tem[8:10],tem[6:8],tem[4:6],tem[2:4],tem[0:2] ]
        address = ['AA','AA','AA','AA','AA','AA']
        code = ['15']
        length = ['06']
        tem1 = ['68']+address+['68']+code+length+dl645.add33H(set_addr)
        crc = dl645.getCheckSum(tem1)
        frame = tem1 + [crc] + ['16']
        return dict(
            frame = frame,
            cmd_info = command,
            sen_fmat = "写通信地址参数为 " + "".join( set_addr[::-1] ),
            rec_fmat = ""
        )

    #读取日期及星期  :get date
    if re.match(r':get date', command):
        address = ADDRESS
        code = ["11"]
        length = ["04"]
        data = ["01","01","00","04"]  #数据标识已按从高到底处理
        tem = ['68']+address+['68']+code+length+dl645.add33H(data)
        crc = dl645.getCheckSum( tem )
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+校验和+16
        frame = tem + [crc] + ['16']
        return dict(
			frame = frame,
            cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
            sen_fmat = "",
            rec_fmat = "抄读日期及星期为 20{0[14]}{0[15]}-{0[12]}{0[13]}-{0[10]}{0[11]} 星期{0[8]}{0[9]}"
		)

    #写日期及星期   :set date YYMMDDWW
    if re.match(r':set date ', command):
        data_id =  ["01","01","00","04"]
        password = ["04","11","11","11"]
        operator = ["01","00","00","00"]
        tem = command.split()[2] #提取时间参数
        #####################这段代码有问题，当用户输入参数长度不足时会报错
        set_date = [ tem[6:8], tem[4:6], tem[2:4], tem[0:2] ]
        address = ADDRESS
        code = ["14"]
        length = ["10"]
        tem1 = ['68']+address+['68']+code+length+dl645.add33H(data_id+password+operator+set_date)
        crc = dl645.getCheckSum(tem1)
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+密码+操作者代码+时间参数+校验和+16
        frame = tem1 + [crc] + ['16']
        return dict(
            frame = frame,
            cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data_id[::-1] ) ),
            sen_fmat = "写日期及星期参数为 " + "".join( set_date[::-1] ),
            rec_fmat = ""
        )
    
    #抄读需量  :get demand xx,xx,xx  
    #参数1：正向有功、反向有功、组合无功I、组合无功II、第1、2、3、4象限无功
    #参数2：总，费率1、2、3、4、5、6、7、8，块
    #参数3：本月，上1、2、3、4、5、6、7、8、9、10、11、12月
    if re.match(r':get demand ', command):
        ptem = command.split()[2].split(',')  #提取参数数组
        dmdInfo = dl645.getDmdEngItem(ptem)
        address = ADDRESS
        code = ["11"]
        length = ["04"]
        data = ptem[::-1] + ["01"]  #数据标识已按从高到底处理
        tem = ['68']+address+['68']+code+length+dl645.add33H(data)
        crc = dl645.getCheckSum( tem )
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+校验和+16
        frame = tem + [crc] + ['16']
        '''数据块和非数据块分开返回'''
        if not isinstance(dmdInfo, list): #非数据块 
            return dict(
		        frame = frame,
                cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
                sen_fmat = dmdInfo+"最大需量及发生时间\t",
                rec_fmat = "{0[12]}{0[13]}.{0[10]}{0[11]}{0[8]}{0[9]}"+\
                        ",{0[22]}{0[23]}{0[20]}{0[21]}{0[18]}{0[19]}{0[16]}{0[17]}{0[14]}{0[15]}"
		    )
        else:   #数据块
            '''关于数据块设计主要看两个参数
            sen_fmat有原来的字符串改为字符串list，返回结果如果判断是list类型就会认为是数据块抄读
            rec_fmat也为list数组，分别对应每一项的显示格式，这么做的目的是增加通用性，因为事件记
            录等块抄数据项每一项内容长度不一致;
            item_len 块抄新增list数组，分别代表块数据每一项的字符串长度，这么做的目的是增加通用性，
            因为事件记录等块抄数据项每一项内容长度不一致'''
            return dict(
                frame = frame,
                cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
                sen_fmat = [i+"最大需量及发生时间\t" for i in dmdInfo], #数据块对应的全部项目
                rec_fmat = ["{0[4]}{0[5]}.{0[2]}{0[3]}{0[0]}{0[1]}"+\
                        ",{0[14]}{0[15]}{0[12]}{0[13]}{0[10]}{0[11]}{0[8]}{0[9]}{0[6]}{0[7]}"]*9, #数据块每一项输出格式
                rec_item = [16]*9  #数据块每一项对应的字符长度
            )            

    #抄读电量 :get energy xx,xx,xx  
    #参数1：正向有功、反向有功、组合无功I、组合无功II、第1、2、3、4象限无功
    #参数2：总，费率1、2、3、4、5、6、7、8，块
    #参数3：本月，上1、2、3、4、5、6、7、8、9、10、11、12月
    if re.match(r':get energy ', command):
        ptem = command.split()[2].split(',')  #提取参数数组
        dmdInfo = dl645.getDmdEngItem(ptem)
        address = ADDRESS
        code = ["11"]
        length = ["04"]
        data = ptem[::-1] + ["00"]  #数据标识已按从高到底处理
        tem = ['68']+address+['68']+code+length+dl645.add33H(data)
        crc = dl645.getCheckSum( tem )
        #帧格式：68+通信地址+68+控制码+数据长度+数据标识+校验和+16
        frame = tem + [crc] + ['16']
        '''数据块和非数据块分开返回'''
        if not isinstance(dmdInfo, list): #非数据块 
            return dict(
		        frame = frame,
                cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
                sen_fmat = dmdInfo+"电能\t",
                rec_fmat = "{0[14]}{0[15]}{0[12]}{0[13]}{0[10]}{0[11]}.{0[8]}{0[9]}"
		    )
        else:   #数据块
            '''关于数据块设计主要看两个参数
            sen_fmat有原来的字符串改为字符串list，返回结果如果判断是list类型就会认为是数据块抄读
            rec_fmat也为list数组，分别对应每一项的显示格式，这么做的目的是增加通用性，因为事件记
            录等块抄数据项每一项内容长度不一致;
            item_len 块抄新增list数组，分别代表块数据每一项的字符串长度，这么做的目的是增加通用性，
            因为事件记录等块抄数据项每一项内容长度不一致'''
            return dict(
                frame = frame,
                cmd_info = command + "\t[功能码:{:^11}]".format( " ".join( data[::-1] ) ),
                sen_fmat = [i+"电能\t" for i in dmdInfo], #数据块对应的全部项目
                rec_fmat = ["{0[6]}{0[7]}{0[4]}{0[5]}{0[2]}{0[3]}.{0[0]}{0[1]}"]*9, #数据块每一项输出格式
                rec_item = [8]*9  #数据块每一项对应的字符长度
            )            
    
    if dl645.isValid(command.split()):  #如果输入直接为协议帧格式
        return dict(
            frame = command.split(),
            cmd_info = "",
            sen_fmat = "",
            rec_fmat = ""
        )
   
    if True:
        if command != "":   #命令不为空则报错
            return dict(
                frame = None,
                sen_fmat = ">命令未封装或不存在,请检查...\n",
                rec_fmat = ""
            )
        
        return dict(         #直接输入回车则输出区域也跟着换行，且不报任何错误
            frame = None,
            sen_fmat = "\n",
            rec_fmat = ""
        )

#发送命令到串口并打印返回信息，用于在执行脚本过程中直接下发封装命令，类似navigator中脚本执行方式的tsend命令
def psend(command):
    cmd_in = encapCmd(command)
    if cmd_in['frame'] != None:    #命令解析没有返回None表示命令解析成功
        output = dl645.sendCmd( dl645.toCOM( cmd_in['frame'] ) ) 
        cmd_out = dl645.toHex(output)
        runinfo = showResult(command, cmd_in, cmd_out)
    else:
        runinfo = cmd_in['sen_fmat'] 

def showResult(command, cmd_in, cmd_out):
    '''回显格式如下：
    ==================================================================================
    [YYYY-MM-DD hh:mm:ss] -------操作时间记录
    :get time [功能码: 04 00 01 02]     ---显示命令+功能码
    XXXXXXX  XXXXXXXXXXXXX              ---抄读值或设置值显示，允许多行
    发: 68 11 11 11 11 11 11 68 11 04 35 34 33 37 1E 16
    收: 68 11 11 11 11 11 11 68 91 07 35 34 33 37 36 6C 3B 7E 16
    命令执行成功！/异常应答帧/... --------操作成功及状态记录
    '''
    result = []  #result用于记录回显信息并返回

    #操作时间记录[YYYY-MM-DD hh:mm:ss]
    operate_time = time.strftime("[%Y-%m-%d %H:%M:%S]")
    result.append( "{:=^100}".format(operate_time) + '\n' )
    print(result[-1], end='')

    #发送命令信息记录
    result.append( cmd_in['cmd_info'] + "\n" )
    print(result[-1], end='')

    '''encapCmd函数的返回格式区分为：发送格式显示信息sen_fmat、接收格式返回信息rec_fmat
    1.报文有应答帧且收到应答显示：sen_fmat + rec_fmat.format(data_area);
    2.报文无应答帧或没有收到应答或异常应发帧显示: sen_fmat;
    '''
    if ( len(cmd_out) > 0 ) and ( int(cmd_out[8], 16)&0x40 == 0 ): #收到应答帧且非异常应答帧
        #只有在返回正常应答帧帧的情况下才需要处理数据域
        #对返回帧数据域进行减33H处理，但是需要对参数合法性进行检查
        data_area = dl645.minus33H(cmd_out[10:-2])  
        tem = "".join(data_area)
        if not isinstance(cmd_in['sen_fmat'], list):
            result.append( cmd_in['sen_fmat'] + cmd_in['rec_fmat'].format(tem) + "\n" )
            print(result[-1], end='')
        else:
            block_item = dl645.splitByLen(tem[8:],cmd_in['rec_item'])
            for i in range(len(block_item)):
                result.append( cmd_in['sen_fmat'][i] + cmd_in['rec_fmat'][i].format(block_item[i]) + "\n" )
                print(result[-1], end='')
    else:               #无应答帧
        if not isinstance(cmd_in['sen_fmat'], list):
            result.append( cmd_in['sen_fmat'] + "\n" )
            print(result[-1], end='')
        else:
            for i in cmd_in['sen_fmat']:
                result.append(i + "\n")
                print(result[-1], end='')

    #发送帧信息 发: 68 11 11 11 11 11 11 68 11 04 35 34 33 37 1E 16
    result.append( "发:"+" ".join( cmd_in['frame'] ) + '\n' )
    print(result[-1], end='')

    #接收帧信息 收: 68 11 11 11 11 11 11 68 91 07 35 34 33 37 36 6C 3B 7E 16
    result.append( "收:"+" ".join( cmd_out ) + '\n' )
    print(result[-1], end='')

    #命令执行结果记录
    if len(cmd_out) > 0:
        if int(cmd_out[8], 16) & 0x40 == 0: #收到正常应答帧
            result.append( "命令执行成功!" + "\n" )
            print(result[-1], end='')
            if re.findall(r'et address', command):
                global ADDRESS   #如果未加global全局变量声明，则会被认为是局部变量
                ADDRESS = cmd_out[1:7]
        else:
            #错误信息没有考虑扩展协议的情况，扩展协议下会报错
            result.append( "异常应答帧!\t" + "{:*^20}".format( dl645.getError(cmd_out[-3]) ) + "\n" )
            print(result[-1], end='')
    else:
        result.append( "无应答" + "\n" )
        print(result[-1], end='')
    return result


if __name__ == '__main__':
    while True:
        incmd = input(">>>")
        exec(incmd) 
        if input == "exit":
            break
