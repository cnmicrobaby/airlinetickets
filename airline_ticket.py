import requests
import json

from prettytable import PrettyTable


class TrainsCollection:
    header = '航空公司 航班 出发地 到达地 机场 时间 价格 余票'.split()

    def __init__(self, airline_tickets):
        self.airline_tickets = airline_tickets

    @property
    def plains(self):
        for item in self.airline_tickets:
            airline_data = [
                item["airlineName"],
                item["flightNumber"],
                item["departureCityName"],
                item["arrivalCityName"],
                '\n'.join([item["departureAirportName"] + item["departureTerminalName"],
                           item["arrivalAirportName"] + item["arrivalTerminalName"]]),
                '\n'.join([item["departureDate"],
                           item["arrivalDate"]]),
                item["price"],
                item["seatCount"]
            ]
            yield airline_data

    def pretty_print(self):
        pt = PrettyTable()
        pt.field_names = self.header
        for airline_data in self.plains:
            pt.add_row(airline_data)
        pt.align = "c"
        print(pt.get_string(sortby="时间"))


def getResponse(fromCity, toCity, tripDate):
    url = "https://flights.ctrip.com/itinerary/api/12808/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Referer": "https://flights.ctrip.com/international/search/",
        "Content-Type": "application/json"
    }
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {"dcity": fromCity, "acity": toCity, "date": tripDate}
        ]
    }
    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers).text
    return response


def parseInfo(fromCity, toCity, tripDate):
    airInfoList = []
    response = getResponse(fromCity, toCity, tripDate)
    # 很多航班信息在此分一下
    routeList = json.loads(response).get('data').get('routeList')
    # 依次读取每条信息
    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        airplaneInfo = {}
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # 提取想要的信息
            airlineName = flight.get('airlineName')  # 航空公司
            flightNumber = flight.get('flightNumber')  # 航班编号
            departureDate = flight.get('departureDate')  # 出发时间
            arrivalDate = flight.get('arrivalDate')  # 到达时间
            craftTypeName = flight.get('craftTypeName')  # 飞机类型
            craftTypeKindDisplayName = flight.get('craftTypeKindDisplayName')  # 飞机型号：大型；中型，小型
            departureCityName = flight.get('departureAirportInfo').get('cityName')  # 出发城市
            departureAirportName = flight.get('departureAirportInfo').get('airportName')  # 出发机场名称
            departureTerminalName = flight.get('departureAirportInfo').get('terminal').get('name')  # 出发机场航站楼
            arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')  # 到达城市
            arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')  # 到达机场名称
            arrivalTerminalName = flight.get('arrivalAirportInfo').get('terminal').get('name')  # 到达机场航站楼
            punctualityRate = flight.get('punctualityRate')  # 到达准点率
            mealType = flight.get('mealType')  # 是否有餐食  None：代表无餐食，Snack：代表小食，Meal：代表含餐食
            cabins = legs[0].get('cabins')
            price = cabins[0].get('price').get('price')  # 标准价格
            rate = cabins[0].get('price').get('rate')  # 折扣率
            seatCount = cabins[0].get('seatCount')  # 剩余座位数
            refundEndorse = cabins[0].get('refundEndorse').get('minRefundFee')  # 成人票：产品退订费
            minEndorseFee = cabins[0].get('refundEndorse').get('minRefundFee')  # 成人票：产品更改费
            endorseNote = cabins[0].get('refundEndorse').get('endorseNote')  # 成人票：签转条件
            freeLuggageAmount = cabins[0].get('freeLuggageAmount')  # 免费托运重量
            carryonLuggageMaxAmount = cabins[0].get('luggageLimitation').get('carryonLuggageMaxAmount')
            # 允许携带手提行李最大数量    0：代表无免费行李额，1：代表一件，-2：代表不限件数
            carryonLuggageMaxWeight = cabins[0].get('luggageLimitation').get('carryonLuggageMaxWeight')  # 允许携带手提行李最大重量
            carryonLuggageMaxSize = cabins[0].get('luggageLimitation').get('carryonLuggageMaxSize')  # 允许携带手提行李最大规格
            checkinLuggageMaxAmount = cabins[0].get('luggageLimitation').get('checkinLuggageMaxAmount')
            # 允许托运的行李最大数量类型   0：代表无免费行李额，1：代表一件，-2：代表不限件数
            checkinLuggageMaxWeight = cabins[0].get('luggageLimitation').get('checkinLuggageMaxWeight')  # 允许托运的行李最大重量
            checkinLuggageMaxSize = cabins[0].get('luggageLimitation').get('checkinLuggageMaxSize')  # 允许托运的行李最大规格
            characteristic = legs[0].get('characteristic')
            lowestPrice = characteristic.get('lowestPrice')  # 成人经济舱最低价
            lowestCfPrice = characteristic.get('lowestCfPrice')  # 成人公务舱最低价
            lowestChildPrice = characteristic.get('lowestChildPrice')  # 儿童经济舱最低价
            lowestChildCfPrice = characteristic.get('lowestChildCfPrice')  # 儿童公务舱最低价
            # 将数据放入字典
            airplaneInfo["airlineName"] = airlineName
            airplaneInfo["flightNumber"] = flightNumber
            airplaneInfo["departureDate"] = departureDate
            airplaneInfo["arrivalDate"] = arrivalDate
            airplaneInfo["craftTypeName"] = craftTypeName
            airplaneInfo["craftTypeKindDisplayName"] = craftTypeKindDisplayName
            airplaneInfo["departureCityName"] = departureCityName
            airplaneInfo["departureAirportName"] = departureAirportName
            airplaneInfo["departureTerminalName"] = departureTerminalName
            airplaneInfo["arrivalCityName"] = arrivalCityName
            airplaneInfo["arrivalAirportName"] = arrivalAirportName
            airplaneInfo["arrivalTerminalName"] = arrivalTerminalName
            airplaneInfo["punctualityRate"] = punctualityRate
            airplaneInfo["mealType"] = mealType
            airplaneInfo["price"] = price
            airplaneInfo["rate"] = rate
            airplaneInfo["seatCount"] = seatCount
            airplaneInfo["refundEndorse"] = refundEndorse
            airplaneInfo["minEndorseFee"] = minEndorseFee
            airplaneInfo["endorseNote"] = endorseNote
            airplaneInfo["freeLuggageAmount"] = freeLuggageAmount
            airplaneInfo["carryonLuggageMaxAmount"] = carryonLuggageMaxAmount
            airplaneInfo["carryonLuggageMaxWeight"] = carryonLuggageMaxWeight
            airplaneInfo["carryonLuggageMaxSize"] = carryonLuggageMaxSize
            airplaneInfo["checkinLuggageMaxAmount"] = checkinLuggageMaxAmount
            airplaneInfo["checkinLuggageMaxWeight"] = checkinLuggageMaxWeight
            airplaneInfo["checkinLuggageMaxSize"] = checkinLuggageMaxSize
            airplaneInfo["lowestPrice"] = lowestPrice
            airplaneInfo["lowestCfPrice"] = lowestCfPrice
            airplaneInfo["lowestChildPrice"] = lowestChildPrice
            airplaneInfo["lowestChildCfPrice"] = lowestChildCfPrice
            # 添加机票信息到列表中
            airInfoList.append(airplaneInfo)
    return airInfoList
