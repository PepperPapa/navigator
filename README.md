# navigator
a simple automatic test GUI tool for electrical meter.
一个轻量级的电能表自动化测试工具

本次重构实现目标：
1.通过json格式实现表计命令的存储和读取
2.实现表计命令可扩展，增加表计命令无需修改代码，一条命令一个封装，虽然命令比较多，但是可以做到没有耦合
3.实现模块化，每个模块实现一组特定的功能
4.针对每个模块编写测试代码

包含模块及功能描述：
1.GUI显示模块navigator.py: 实现表计测试工具GUI界面
2.表计协议处理模块meter.py: 实现表计通信帧的生成及显示等处理
3.表计封装命令文件处理模块cmd.py: 实现表计封装命令的添加、读取、存储，采用json格式
4.485通信处理模块rs485.py: 实现表计485通信
5.日志记录模块log.py: 实现日志文件的记录
6.测试脚本处理模块testcase.py: 实现测试用例的保存、另存、读取




========================old===========================
绿色-已完成；黑色-进行中；红色-取消

1.使用VBA实现三晖台体导出的误差原始数据转移到三相表测试数据模板中，代替手工作业。----目前已经通过vlookup函数实现，不需要使用VBA。
2.使用python开发一个命令行程序-电表通信助手：手工输入电能表可以识别的报文，发给串口，显示读出的数据，即一个简单的发送和接收小工具。
?????20150515:目前已基本完成，只需要再处理一下读串口数据的显示为十六进制即可完成。
? ? ?20150518:已经完成，通过和310的执行结果进行验证，发送正确的命令即可打印电表返回的结果，且显示形式和310完全一致。? ?
3.使用python开发一个帧解析程序：手工输出电能表可以识别的报文，通过程序处理可以打印报文的详细解析信息和值，主要工作量：通信协议帧的所有类型解析，工作量大，体现想好架构，一步步实现，不要追求完美，先追求可用。
? ? ?20150608-已完成电能量和需量除块外抄读部分的帧解析，下一步需把电能量和需量的块抄读解析搞定
? ? ?20150714-目前完成电能量和需量部分（包括块）帧的解析，由于类navigator工具可以根据输入命令得出返回帧的信息，所以这部分工作实际上是多余的，项目暂停，后续如有需求再实现，不做没用的事情。
5.开发自己的自动化测试工具。
? ? ?20150428：目前已经做到使用IPOP工具连接到串口，发送电表能识别的任意命令均可以输出回应报文，但是IPOP输出窗口显示为乱码，需要找到解决办法；
? ? ?20150506：由于找不到更合适的现成工具，决定使用python语言来自己开发。先通过开发一些小的简单的工具，等python语言掌握的比较好之后开始逐步搭建自动化测试的架构。
6.逐渐建立起自己的测试用例库，暂时可以考虑使用excel来做，要做到测试点明确、测试步骤清晰，用例设计合理，能够覆盖大部分的功能测试。如果能够以后根据这个用例库做出自动测试用例更好，不过一开始不要求完美，慢慢积累。
7.完成一个python脚本最好能通过批处理的方式执行，做到每次写周报的时候双击一个文件就能够创建一个最新的一次周报的副本并按照相同的规则进行命名，不再需要手工去修改文件名。（20150308）
20150608---已完成
8.为电表通信助手程序开发GUI界面。(20150610--已完成并发布，eMeter_Assistant.py)



4.使用python开发一个命令行程序：要求GUI界面，把电能表的帧命令形式封装成易懂的命令+参数形式，类似与华为的navigator工具，主要工作量：命令的封装
(需求分析： version 1.0
1.命令输入窗口要既可以支持python脚本运行（右键执行选中脚本，菜单选项run执行全部脚本），也可以支持按封装好的命令方式执行选中命令或当前光标所在行命令（Ctrl+Shift或其他易用的按键）执行。
2.输出命令应能实时以日志保存，执行命令应记录操作时间已备回溯。
3.输入命令或脚本窗口的命令或脚本可以通过菜单进行保存或打开。
4.工具可以设置电表通信端口，超时时间、台体通信参数设置（下个版本）。
5.输入区域支持python脚本语法高亮，自动缩进。
6.电表通信命令封装完成，可以逐步积累实现。
7.支持直接按原始帧方式发送命令执行并返回帧。
8.状态栏实时显示当前系统时间
遗留问题：如何实现自己的工具能够执行并输出python脚本？? ? ---已解决
20150714-已经开发出雏形，实现了GUI界面，能够执行时间、日期、通信地址的读取和设置。（厂内）；实现了输入命令Text区域语法高亮显示。
20150715-对程序的GUI布局进行了优化，实现了一个类Navigator的界面。实现输出日志记录功能（输出结果实时记录到txt文件中，存在路径：当前目录下log文件夹下，文件名：log+年月日时分秒）
20150717-对程序的结构进行了优化，根据功能分成多文件组织程序，使程序结构更加清晰
20150727-已经实现了在GUI工具中执行python脚本的功能，关键技术可以说全部解决了。
20150731-中间有遇到了text组件不能实时刷新exec执行结果的问题，经过反复验证和推测发现是text写入文本后需要执行text.update()即可解决。另外，已经实现psend命令，目前命令方式执行和脚本方式执行均已实现。
20150901-已经实现了测试脚本的打开、保存、另存为功能。
20150918：
-优化了log记录功能：如果打开navigator没有打印任何信息则不需要建立log文件，可以减少无存储无效的log文件
-优化了navigator界面状态栏窗口伸缩可能无法显示的问题 ? ?
-增加了状态栏实时显示年月日时分秒的功能，方便校对表计时间时可以对照
-实现了navigator调用退出函数方法，可以在退出前执行自定义的功能

20150921:
-实现输出打印区域如果出现异常应答帧或无应答时，相应的信息以红色字体显示以提示测试人员注意

=======================================[2015-07-30 10:50:22]========================================
:get time???? [功能码:04 00 01 02]
抄读时间为 E9:09:E1
发:68 02 00 00 00 00 00 68 11 04 35 34 33 37 BA 16
收:68 02 00 00 00 00 00 68 91 07 35 34 33 37 14 3C 1C A9 16
命令执行成功!
=======================================[2015-07-30 10:50:24]========================================
:get date???? [功能码:04 00 01 01]
抄读日期及星期为 202C-55-C8 星期05
发:68 02 00 00 00 00 00 68 11 04 34 34 33 37 B9 16
收:68 02 00 00 00 00 00 68 91 08 34 34 33 37 38 FB 88 5F 57 16
命令执行成功!

发：68 01 00 00 00 00 00 68 11 04 34 34 33 37 B8 16
收：68 01 00 00 00 00 00 68 91 08 34 34 33 37 38 58 3C 48 50 16
日期及星期:操作成功!
响应延时:197毫秒
发：68 01 00 00 00 00 00 68 11 04 35 34 33 37 B9 16
收：68 01 00 00 00 00 00 68 91 07 35 34 33 37 3C 8A 43 45 16
时间:操作成功!
响应延时:209毫秒

20150925：
-根据谷歌python编码规范，初步修改编码风格使其尽量符合谷歌的编码风格，随着理解的进一步加深还需要进一步完善编码风格

20151116：
-对当前代码进行重构，目标是要做到命令的可扩展，增加表计命令不需要更改代码，这样的话表计自动测试工具就是一个框架，
不需要封装所有的命令，测试期间可以逐步添加所需要的命令而不需要工具有任何改变，极大提高了测试工具的可扩展性，计划通过json来实现对命令的解析，并本地保存
