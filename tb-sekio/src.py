import frida
import sys


def on_message(message, data):
    if message['type'] == 'send':
        print("*****[frida hook]***** : {0}".format(message['payload']))
    else:
        print("*****[frida hook]***** : " + str(message))


def get_javascript(filepath):
    code = ''
    with open(filepath, 'r') as file:
        code = code + file.read()
    return code


# 连接远端设备
device = frida.get_remote_device()
# 附加到进程
session = device.attach("淘宝")
# 1、直接写入 javascript 代码
javascript = """
Java.perform(function () {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
        var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        console.log("isGlobalSpdySwitchOpenl " + ret)
        return false
    }
})
"""
# 2、从文件中加载 javascript 脚本代码
# javascript = get_javascript(javascript_file)
# 基于脚本内容创建运行脚本对象
script = session.create_script(javascript)
script.on('message', on_message)
# 加载脚本并执行
script.load()
sys.stdin.read()
