# python3.4
# dl645.py
# 645协议相关的处理
import math
import serial
#import copy

energy_type = {
            '00': '组合有功',
            '01': '正向有功',
            '02': '反向有功',
            '03': '组合无功I',
            '04': '组合无功II',
            '05': '第一象限无功',
            '06': '第二象限无功',
            '07': '第三象限无功',
            '08': '第四象限无功',
            '15': 'A相正向有功',
            '16': 'A相反向有功',
            '17': 'A相组合无功I',
            '18': 'A相组合无功II',
            '19': 'A相第一象限无功',
            '1A': 'A相第二象限无功',
            '1B': 'A相第三象限无功',
            '1C': 'A相第四象限无功',
            '1C': 'A相第一象限无功',
            '29': 'B相正向有功',
            '2A': 'B相反向有功',
            '2B': 'B相组合无功I',
            '2C': 'B相组合无功II',
            '2D': 'B相第一象限无功',
            '2E': 'B相第二象限无功',
            '2F': 'B相第三象限无功',
            '30': 'B相第四象限无功',
            '3D': 'C相正向有功',
            '3E': 'C相反向有功',
            '3F': 'C相组合无功I',
            '40': 'C相组合无功II',
            '41': 'C相第一象限无功',
            '42': 'C相第二象限无功',
            '43': 'C相第三象限无功',
            '44': 'C相第四象限无功'
        }

rate_type = ('总','费率1','费率2','费率3','费率4','费率5',
            '费率6','费率7','费率8')

month_type = {
            '00': '(当前)',
            '01': '(上1月)',
            '02': '(上2月)',
            '03': '(上3月)',
            '04': '(上4月)',
            '05': '(上5月)',
            '06': '(上6月)',
            '07': '(上7月)',
            '08': '(上8月)',
            '09': '(上9月)',
            '0A': '(上10月)',
            '0B': '(上11月)',
            '0C': '(上12月)'
        }
error_name = {
            '01': '其他错误',
            '02': '无请求数据',
            '04': '密码错/未授权',
            '08': '通信速率不能更改',
            '10': '年时区数超',
            '20': '日时段数超',
            '40': '费率数超'
        }

#电表通信参数全局变量
MeterPara = {'com': 'COM5', 'baudrate': 2400, 'datasize': 8, 'stopbits': 1, 'parity': 'E', 'timeout': 0.5}   

def toCOM(cmd_list):
    '''用户输入数据处理为写入串口的list数据
    把输入命令转换为serial.write函数能接受的整数list类型
    inData: 为字符串list类型，如['68', '11', '11', '11', '11', '11', '11', '68', \
		    '11', '04', '35', '34', '33', '37', '1E', '16']
    '''
    return [int(i, 16)  for i in cmd_list]

def toHex(read_from_COM):
    '''串口读出的数据处理为十六进制显示方式
    read_from_COM: bytes类型'''
    return ["{0:02X}".format(i) for i in read_from_COM] 
	
def sendCmd(cmd):
    global MeterPara
    rs485 = serial.Serial(MeterPara['com'], MeterPara['baudrate'], parity=MeterPara['parity'], timeout=MeterPara['timeout'])
    rs485.write( cmd  )    #发送命令到串口，write函数只能接收整数list类型参数'''
    outStr = rs485.read(212)	  #根据645规定计算帧长最大不会超过212字节
    rs485.close()
    return outStr

def minus33H(data_list):
    '''数据域作减33h处理，接收数据使用
    data_list:[xx,xx,xx,...]
    '''
    fm = data_list
    # 减33h等于加上33h的补码cdh，补码为反码加1
    tem = [math.fmod( ( int(i, 16) + int('cd', 16) ), 256) for i in fm]   
    for i in range(len(tem)):
    #十进制格式化为十六进制显示,format参数不能为float类型
        tem[i] = "{0:02X}".format( int( tem[i] ) )
    return tem

def add33H(data):
    '''数据域作加33h处理，接收数据使用
    data_list:[xx,xx,xx,...]
    '''
    fm = data
    tem = [math.fmod( ( int(i, 16) + int('33', 16) ), 256) for i in fm]   
    for i in range(len(tem)):
    #十进制格式化为十六进制显示,format参数不能为float类型
        tem[i] = "{0:02X}".format( int( tem[i] ) )
    return tem

def getCheckSum(data):
    '''根据用户输入的帧信息计算出校验和，并返回计算的校验和的值，以16进制字符串形式返回
    校验和计算方法：等于除结束符、校验码以外的所有字节的十进制数之和与256的模,以十六进制形式体现在报文中
    data: 为字符串list类型，如['68', '11', '11', '11', '11', '11', '11', '68', 
		    '11', '04', '35', '34', '33', '37', '1E', '16']
    '''
    #tem = copy.copy(data)   # list是引用方式传递参数，会修改报文的内容，创建一份copy不会改变原数据的值
    #以下语句可以代替copy.copy功能，待验证...
    tem = list(data) 
    # 将copy后的list值转换为10进制
    tem = [int(i, 16) for i in tem]   #列表推导
    return "{0:02X}".format(  int( math.fmod( sum( tem[:] ), 256  )  )  ) #计算的校验和

# 检查帧起始符、结束符、校验和，判断是否是有效帧
def isValid(frame):
    '''检查帧起始符、结束符、校验码是否是正确的值，
    正确则报文有效，返回True，否则报文无效，返回False'''
    if len(frame) < 12: #协议最短帧长为12字节，不足12字节直接返回None
        return None
    if (frame[0] != '68') and (frame[7] != '68') and (frame[-1] != '16'): #起始符、结束符错误直接返回None
        return None 
    if int(frame[9], 16) != len(frame[10:-2]): #数据域长度和实际数据域长度不符直接返回None
        return None
    if getCheckSum(frame[0:-2]) != frame[-2]: #校验码错误直接返回None 
        return None 
    return True   #以上都符合要求则返回True 

def getDmdEngItem(id_list):  
    #根据数据标识获取需量或电量的数据信息，正向有功总、组合有功费率1、等
    # id_list: [xx,xx,xx] 
    #参数1：正向有功、反向有功、组合无功I、组合无功II、第1、2、3、4象限无功
    #参数2：总，费率1、2、3、4、5、6、7、8，块
    #参数3：本月，上1、2、3、4、5、6、7、8、9、10、11、12月

    #如果是数据块则以list形式返回
    if id_list[1].upper() == 'FF':
        return [month_type[ id_list[2].upper() ] + \
                    energy_type[ id_list[0].upper() ] + i \
                    for i in rate_type ]
    else:
        return month_type[ id_list[2].upper() ] \
            + energy_type[ id_list[0].upper() ] \
            + rate_type[ int( id_list[1] ) ] 

def getError(err_data):
    #收到异常应答帧，获取具体的错误信息
    #err_data: 为异常应答帧的ERR字节
    #目前仅支持07协议错误信息，不支持国网第4号补遗文件扩展的错误信息，暂会报错
    err = minus33H( [err_data] ) 
    return error_name[ err[0] ]

def splitByLen(string, len_list):
    '''
    string: 要分割的字符串
    len_list:字符串长度数据
    如string="1234567890",len_list=[2,4,3,1]
    则函数返回['12', '3456', '789', '0']
    '''
    for i in range(len(len_list)):
        if i > 0:
            len_list[i] += len_list[i-1]
    tem = []
    for i in range(len(len_list)):
        if i == 0:
            tem.append( string[0:len_list[i]] )
        else:
            if len_list[i] > len(string):  #限制大于字符串长度后结束返回
                continue
            else:
                tem.append( string[ len_list[i-1]:len_list[i] ] )
    return tem

