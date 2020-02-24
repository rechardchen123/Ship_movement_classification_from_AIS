import os
import operator

directory = r'C:\Users\LPT-ucesxc0\AIS-Data\Danish_AIS_data_process\split_data\aisdk_20180905_split_abnormal_ais'  # 需要修改的工作目录
os.chdir(directory)  # 改变当前工作目录
cwd = os.getcwd()  # 查看当前工作目录
print("--------------current working directory : " + cwd + "----------")


def deleteBySize(minSize):
    '''
    :param minSize:
    :return:删除指定大小的文件
    '''
    files = os.listdir(os.getcwd())  # 列出目录中的文件
    for file in files:
        if os.path.getsize(file) < minSize * 1024:
            os.remove(file)
            print(file + " was deleted.")
    return


def deleteNullFile():
    '''
    删除大小为0的文件
    :return:
    '''
    files = os.listdir(os.getcwd())
    for file in files:
        if os.path.getsize(file) == 1:
            os.remove(file)
            print(file + " was deleted.")
    return


hint = '''funtion : 
        1    delete null file
        2    delete by size
        q    quit\n
please input number: '''

while True:
    option = input(hint)
    if option == '1':
        deleteNullFile()
    elif option == '2':
        minSize = int(input("minSize(k):"))  # 键盘输入的是字符串，需要强制转换成int类型
        deleteBySize(minSize)
    elif option == 'q':
        print("quit !")
        break
    else:
        print("disabled input. please try again...")
