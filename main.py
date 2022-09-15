import json
import requests

DATA_SET = {}

adcode = 0
PROVINCE_ENDPOINT   = f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/100000_province.json"
CITY_ENDPOINT       = f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/{adcode}_city.json"
DISTRICT_ENDPOINT   = f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/{adcode}_district.json"


def get_district_list(adcode):
    res = requests.get(f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/{adcode}_district.json")
    try:
        district_list = json.loads(res.content.decode())['rows']
    except Exception as e:
        print(f"Error getting district list:\nError: {e}\nData: {res.content}")
        district_list = []
    else:
        district_list = [r['name'] for r in district_list]
    print(f"status code :{res.status_code}\tfound districts: {len(district_list)}")
    return district_list


def get_city_list(adcode):
    res = requests.get(f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/{adcode}_city.json")
    try:
        city_list = json.loads(res.content.decode())['rows']
    except Exception as e:
        print(f"Error getting city list:\nError: {e}\nData: {res.content}")
        city_list = []
    print(f"status code :{res.status_code}\tfound cities: {len(city_list)}")
    return city_list


def get_data_set():
    res = requests.get(f"https://datavmap-public.oss-cn-hangzhou.aliyuncs.com/areas/csv/100000_province.json")
    province_list = json.loads(res.content.decode())['rows']
    # province_list = [r['name'] for r in province_list]
    print(f"status code :{res.status_code}\tfound provinces: {len(province_list)}")
    for i, province in enumerate(province_list):
        print(f"# {i+1}. getting cities for province: {province['name']} {province['adcode']}")
        DATA_SET[province['name']] = {}
        city_list = get_city_list(province['adcode'])

        for j, city in enumerate(city_list):
            print(f"## {i+1}.{j+1}. getting district for city: {city['name']} {city['adcode']}")
            DATA_SET[province['name']][city['name']] = get_district_list(city['adcode'])

    json.dump(DATA_SET, open('china_address_input_data_set.json', 'w'), indent=4)


if __name__ == '__main__':
    get_data_set()
