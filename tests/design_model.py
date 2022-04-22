# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 14:50
# @Author  : ZhaoXiangPeng
# @File    : design_model.py

# ! -*- coding: utf-8 -*-

class State:
    # 定义state基类
    def insert_quarter(self):
        pass

    def eject_quarter(self):
        pass

    def turn_crank(self):
        pass

    def dispense(self):
        pass


class SoldOutState(State):
    # 继承State 类
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def __str__(self):
        return "sold_out"

    def insert_quarter(self):
        print("You can't insert a quarter, the machine is sold out")

    def eject_quarter(self):
        print("You can't eject, you haven't inserted a quarter yet")

    def turn_crank(self):
        print("You turned, but ther are no gumballs")

    def dispense(self):
        print("No gumball dispensed")


class SoldState(State):
    # 继承State 类
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def __str__(self):
        return "sold"

    def insert_quarter(self):
        print("Please wait, we're already giving you a gumball")

    def eject_quarter(self):
        print("Sorry, you already turned the crank")

    def turn_crank(self):
        print("Turning twice doesn't get you another gumball")

    def dispense(self):
        self.gumball_machine.release_ball()
        if gumball_machine.count > 0:
            self.gumball_machine.state = self.gumball_machine.no_quarter_state
        else:
            print("Oops, out of gumballs!")
            self.gumball_machine.state = self.gumball_machine.soldout_state


class NoQuarterState(State):
    # 继承State 类
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def __str__(self):
        return "no_quarter"

    def insert_quarter(self):
        # 投币 并且改变状态
        print("You inserted a quarter")
        self.gumball_machine.state = self.gumball_machine.has_quarter_state

    def eject_quarter(self):
        print("You haven't insert a quarter")

    def turn_crank(self):
        print("You turned, but there's no quarter")

    def dispense(self):
        print("You need to pay first")


class HasQuarterState(State):
    # 继承State 类
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def __str__(self):
        return "has_quarter"

    def insert_quarter(self):
        print("You can't insert another quarter")

    def eject_quarter(self):
        print("Quarter returned")
        self.gumball_machine.state = self.gumball_machine.no_quarter_state

    def turn_crank(self):
        print("You turned...")
        self.gumball_machine.state = self.gumball_machine.sold_state

    def dispense(self):
        print("No gumball dispensed")


class GumballMachine:

    def __init__(self, count=0):
        self.count = count
        # 找出所有状态，并创建实例变量来持有当前状态，然后定义状态的值
        self.soldout_state = SoldOutState(self)
        self.no_quarter_state = NoQuarterState(self)
        self.has_quarter_state = HasQuarterState(self)
        self.sold_state = SoldState(self)
        if count > 0:
            self.state = self.no_quarter_state
        else:
            self.state = self.soldout_state

    def __str__(self):
        return ">>> Gumball machine current state: %s" % self.state

    def insert_quarter(self):
        # 投入25分钱
        self.state.insert_quarter()

    def eject_quarter(self):
        # 退回25分
        self.state.eject_quarter()
        # print("state", self.state, type(self.state))

    def turn_crank(self):
        # 转动曲柄
        # print("state", self.state, type(self.state))
        self.state.turn_crank()  # 修改状态
        self.state.dispense()  # 发糖 感谢 @dyq666 指出错误

    def release_ball(self):
        # 发放糖果
        print("A gumball comes rolling out the slot...")
        if self.count > 0:
            self.count -= 1


if __name__ == "__main__":
    # 以下是代码测试
    gumball_machine = GumballMachine(5)  # 装入5 个糖果
    print(gumball_machine)

    gumball_machine.insert_quarter()  # 投入25分钱
    gumball_machine.turn_crank()  # 转动曲柄
    print(gumball_machine)

    gumball_machine.insert_quarter()  # 投入25分钱
    gumball_machine.eject_quarter()  # 退钱
    gumball_machine.turn_crank()  # 转动曲柄

    print(gumball_machine)

    gumball_machine.insert_quarter()  # 投入25分钱
    gumball_machine.turn_crank()  # 转动曲柄
    gumball_machine.insert_quarter()  # 投入25分钱
    gumball_machine.turn_crank()  # 转动曲柄
    gumball_machine.eject_quarter()  # 退钱

    print(gumball_machine)
