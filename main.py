import airline_ticket
import air_stations

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    fromCity = input("输入出发城市：")
    toCity = input("输入到达城市：")
    tripDate = input("输入出发日期：")
    try:
        fromCity = air_stations.stations[fromCity]
        toCity = air_stations.stations[toCity]
        airline_tickets = airline_ticket.parseInfo(fromCity, toCity, tripDate)
        airline_ticket.TrainsCollection(airline_tickets).pretty_print()
    except Exception as e:
        print(e.args)
        print("未查询到相关航班信息，请检查输入信息是否有误！")

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
