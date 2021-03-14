from itertools import product
from tqdm import tqdm
import requests


def chamdiem(importlist):
    available_criteria = [48, 49, 50, 51, 53, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76,
                          77, 78, 79, 94, 95, 96, 97, 98, 99, 100]

    max_criteria_point = {"48": 2, "49": 3, "50": 6, "51": 6, "53": 6, "58": 6, "59": 3, "60": 3, "61": 3, "62": 6,
                          "63": 6, "64": 3,
                          "65": 3, "66": 6, "67": 3, "68": 3, "69": 6, "70": 4, "71": 2, "73": 8, "74": 4, "75": 4,
                          "76": 4, "77": 4,
                          "78": 4, "79": 4, "94": 7, "95": 7, "96": 6, "97": 6, "98": 4, "99": 4, "100": 4}
    max_group_point = {"2": 6, "3": 6, "4": 20, "5": 6, "6": 10, "7": 9, "8": 6, "9": 16, "10": 4}
    max_type_point = {"1": 30, "2": 25, "3": 25, "4": 20}

    group_point = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
    type_point = {"1": 0, "2": 0, "3": 0, "4": 0}

    group_relation = {"2": 1, "3": 1, "4": 2, "5": 2, "6": 3, "7": 3, "8": 3, "9": 4, "10": 4}
    criteria_relation = {"48": 2, "49": 3, "50": 3, "51": 3, "53": 3, "58": 5, "59": 5, "60": 5, "61": 5, "62": 6,
                         "63": 6, "64": 7,
                         "65": 7, "66": 7, "67": 7, "68": 7, "69": 8, "70": 8, "71": 8, "73": 9, "74": 9, "75": 10,
                         "76": 10, "77": 10,
                         "78": 10, "79": 10, "94": 4, "95": 4, "96": 4, "97": 7, "98": 9, "99": 9, "100": 4}

    include_list = {"48": False, "49": False, "50": False, "51": False, "53": False, "58": False, "59": False,
                    "60": False, "61": False, "62": False, "63": False, "64": False, "65": False, "66": False,
                    "67": False, "68": False, "69": False, "70": False, "71": False, "73": False, "74": False,
                    "75": False, "76": False, "77": False, "78": False, "79": False, "94": False, "95": False,
                    "96": False, "97": False, "98": False, "99": False, "100": False}

    for i in importlist.values():
        include_list[str(i)] = True

    # evaluate point
    for i in include_list:
        if (include_list.__getitem__(i)):
            group_point[str(criteria_relation.__getitem__(i))] += max_criteria_point.__getitem__(i)

    # OK till there
    # flatten point
    for i in group_point:
        if (group_point.__getitem__(i) > max_group_point.__getitem__(i)):
            group_point[str(i)] = max_group_point.__getitem__(i)

    # for criteria group
    for i in group_point:
        type_point[str(group_relation.__getitem__(i))] += group_point.__getitem__(i)

    # flatten
    for i in type_point:
        if (type_point.__getitem__(i) > max_type_point.__getitem__(i)):
            type_point[str(i)] = max_type_point.__getitem__(i)

    sum = 0
    for i in type_point:
        sum += type_point.__getitem__(i)
    return sum


# imput data to use
print("Nhập mã số sinh viên: ")
mssv = input()
print("Nhập token: ")
token = input()

# check if session valid
url = "https://ctsv.hust.edu.vn/api-t/User/GetUserInfo"
push_data = {"TokenCode": token, "UserName": mssv}
resp = requests.post(url=url, data=push_data)
json_data = resp.json()

# check responses code
if json_data["RespCode"] != 0:
    print("Có vẻ bạn nhập token không hợp lệ, hoặc phiên đăng nhập đã hết hạn, hoặc web trường bị lỗi. Vui lòng thử "
          "lại token khác")
    exit(0)

# declare global variables
act = {}
data = {'48': [], '49': [], '50': [], '51': [], '53': [], '58': [], '59': [], '60': [], '61': [], '62': [],
        '63': [], '64': [], '65': [], '66': [], '67': [], '68': [], '69': [], '70': [], '71': [], '73': [],
        '74': [], '75': [], '76': [], '77': [], '78': [], '79': [], '94': [], '95': [], '96': [], '97': [], '98': [],
        '99': [], '100': []}
available_criteria = [48, 49, 50, 51, 53, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76,
                      77, 78, 79, 94, 95, 96, 97, 98, 99, 100]

# crawl criteria
print("Đang crawl tiêu chí!")
url = "https://ctsv.hust.edu.vn/api-t/Activity/GetActivityByCId"
for i in tqdm(available_criteria):
    CId = i
    push_data = {"UserCode": mssv, "Signature": "sample string 4", "Search": "", "NumberRow": 30, "CId": CId,
                 "PageNumber": 1, "TokenCode": token, "UserName": mssv}
    resp = requests.post(url=url, data=push_data)
    json_data = resp.json()

    # to append to a dict
    for dty in json_data["Activities"]:
        AId = dty["AId"]
        data[str(i)].append(AId)

# get unique activities that this user join in
result = set({})
for k in data.keys():
    for i in data[k]:
        result.add(i)
unique_act = list(result)

# transmute table to another
for i in unique_act:
    act[i] = []
    for j in data:
        if i in data[j]:
            act[i].append(j)

# get unique key and values of dict to make a Decarter product to brute force
print("Các hoạt động ứng với tiêu chí có thể thêm được: ", act)
keys = act.keys()
vals = act.values()

# BRUTE FORCE!!! Using maximum of compute power to do it
max = 0
max_suit = {}
print("Đang tối ưu!...")
for instance in tqdm(product(*vals)):
    avai = dict(zip(keys, instance))
    current_max = chamdiem(avai)
    if (max < current_max):
        max_suit = avai
        max = current_max

# It is finished!
print("Điểm tối đa đạt được: ", max)
print(max_suit)

point_graded = {"48": [], "49": [], "50": [], "51": [], "53": [], "58": [], "59": [], "60": [], "61": [], "62": [],
                "63": [], "64": [], "65": [], "66": [], "67": [], "68": [], "69": [], "70": [], "71": [], "73": [],
                "74": [], "75": [], "76": [], "77": [], "78": [], "79": [], "94": [], "95": [], "96": [], "97": [],
                "98": [], "99": [], "100": []}
for i in max_suit:
    point_graded[str(max_suit.__getitem__(i))].append(i)

# to print out it
print("Danh sách các tiêu chí ứng với hoạt động: ", point_graded)
