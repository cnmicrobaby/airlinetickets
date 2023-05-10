import airline_ticket
import air_stations

if __name__ == '__main__':
    fromCity = input("输入出发城市：")
    toCity = input("输入到达城市：")
    tripDate = input("输入出发日期（格式：2000-01-01）：")
    try:
        fromCity = air_stations.stations[fromCity]
        toCity = air_stations.stations[toCity]
        airline_tickets = airline_ticket.parseInfo(fromCity, toCity, tripDate)
        airline = airline_ticket.AirlineCollection
        airline(airline_tickets).pretty_print()
    except Exception as e:
        print(e.args)
        print("未查询到相关航班信息，请检查输入信息是否有误！")
