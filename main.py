import Depend
from Config import config
from Core.spider import Waiter
from runserver import running

if __name__ == '__main__':
    choiceList = """
===== 注意 =====
使用前请按要求填写config.ini中的信息

功能列表：                                                                                
 0. 打开面板（选择后使用浏览器打开 http://localhost:12021/）
 1. 自动加购物车，缺货等待上架自动下单
 2. 自动定时加购物车下单（普通商品，非秒杀抢购）
"""
    print(choiceList)
    choice_function = ''
    if choice_function == '':
        choice_function = input('请选择(输入数字):')
    if choice_function == '0':
        print("使用浏览器打开 http://localhost:12021/")
        running()
    elif choice_function == '1':
        waiter = Waiter()
        waiter.waitForSell()
    elif choice_function == '2':
        waiter = Waiter()
        waiter.waitTimeForSell()
    else:
        print('没有此功能')
        exit()

