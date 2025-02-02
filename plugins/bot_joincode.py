"""录取编号
"""
import base64
import os
from EAbotoy import Action, MsgTypes, sugar
from EAbotoy.contrib import plugin_receiver
from EAbotoy.decorators import ignore_botself
from EAbotoy.model import WeChatMsg
from plugins.bot_realname.db import join_real_name

action = Action()

pic_content = str(base64.b64decode(
    'PD94bWwgdmVyc2lvbj0iMS4wIj8+XG48bXNnPlxuXHQ8aW1nIGFlc2tleT0iMzNkN2ViZmMwOTQ4YzJmYmExNjdmNjMwMTFlYmNmMmMiIGVuY3J5dmVyPSIwIiBjZG50aHVtYmFlc2tleT0iMzNkN2ViZmMwOTQ4YzJmYmExNjdmNjMwMTFlYmNmMmMiIGNkbnRodW1idXJsPSIzMDU3MDIwMTAwMDQ0YjMwNDkwMjAxMDAwMjA0NDA0M2Q0ZDUwMjAzMmY4MDI5MDIwNGE3ODMzY2I3MDIwNDYzNDU4NmUyMDQyNDM4MzA2NjMwNjQzODYzNjEyZDY1MzgzNjY1MmQzNDM3NjE2NTJkNjEzMDM2MzQyZDM3MzczMDYxMzYzOTM4NjMzNTYyNjU2MzAyMDQwMTI5MGEwMjAyMDEwMDA0MDUwMDRjNTJhZDAwIiBjZG50aHVtYmxlbmd0aD0iNjk3NyIgY2RudGh1bWJoZWlnaHQ9IjE5OCIgY2RudGh1bWJ3aWR0aD0iOTUiIGNkbm1pZGhlaWdodD0iMCIgY2RubWlkd2lkdGg9IjAiIGNkbmhkaGVpZ2h0PSIwIiBjZG5oZHdpZHRoPSIwIiBjZG5taWRpbWd1cmw9IjMwNTcwMjAxMDAwNDRiMzA0OTAyMDEwMDAyMDQ0MDQzZDRkNTAyMDMyZjgwMjkwMjA0YTc4MzNjYjcwMjA0NjM0NTg2ZTIwNDI0MzgzMDY2MzA2NDM4NjM2MTJkNjUzODM2NjUyZDM0Mzc2MTY1MmQ2MTMwMzYzNDJkMzczNzMwNjEzNjM5Mzg2MzM1NjI2NTYzMDIwNDAxMjkwYTAyMDIwMTAwMDQwNTAwNGM1MmFkMDAiIGxlbmd0aD0iMSIgbWQ1PSJkMGM1MTg0MTZlMWUzMWUxNGRhMzJkYTVlY2MwMmZmNyIgaGV2Y19taWRfc2l6ZT0iNDM3MzIiIC8+XG5cdDxwbGF0Zm9ybV9zaWduYXR1cmU+PC9wbGF0Zm9ybV9zaWduYXR1cmU+XG5cdDxpbWdkYXRhaGFzaD48L2ltZ2RhdGFoYXNoPlxuPC9tc2c+XG4nLCAnU3RhdHVzJzogMywgJ0ltZ1N0YXR1cyc6IDIsICdJbWdCdWYnOiAnLzlqLzRBQVFTa1pKUmdBQkFRQUFBUUFCQUFELzRnSW9TVU5EWDFCU1QwWkpURVVBQVFFQUFBSVlBQUFBQUFJUUFBQnRiblJ5VWtkQ0lGaFpXaUFBQUFBQUFBQUFBQUFBQUFCaFkzTndBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBUUFBOXRZQUFRQUFBQURUTFFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQWxrWlhOakFBQUE4QUFBQUhSeVdGbGFBQUFCWkFBQUFCUm5XRmxhQUFBQmVBQUFBQlJpV0ZsYUFBQUJqQUFBQUJSeVZGSkRBQUFCb0FBQUFDaG5WRkpEQUFBQm9BQUFBQ2hpVkZKREFBQUJvQUFBQUNoM2RIQjBBQUFCeUFBQUFCUmpjSEowQUFBQjNBQUFBRHh0YkhWakFBQUFBQUFBQUFFQUFBQU1aVzVWVXdBQUFGZ0FBQUFjQUhNQVVnQkhBRUlBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRmhaV2lBQUFBQUFBQUJ2b2dBQU9QVUFBQU9RV0ZsYUlBQUFBQUFBQUdLWkFBQzNoUUFBR05wWVdWb2dBQUFBQUFBQUpLQUFBQStFQUFDMnozQmhjbUVBQUFBQUFBUUFBQUFDWm1ZQUFQS25BQUFOV1FBQUU5QUFBQXBiQUFBQUFBQUFBQUJZV1ZvZ0FBQUFBQUFBOXRZQUFRQUFBQURUTFcxc2RXTUFBQUFBQUFBQUFRQUFBQXhsYmxWVEFBQUFJQUFBQUJ3QVJ3QnZBRzhBWndCc0FHVUFJQUJKQUc0QVl3QXVBQ0FBTWdBd0FERUFOdi9iQUVNQUF3SUNBd0lDQXdNREF3UURBd1FGQ0FVRkJBUUZDZ2NIQmdnTUNnd01Dd29MQ3cwT0VoQU5EaEVPQ3dzUUZoQVJFeFFWRlJVTUR4Y1lGaFFZRWhRVkZQL2JBRU1CQXdRRUJRUUZDUVVGQ1JRTkN3MFVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRlAvQUFCRUlBTVlBWHdNQklnQUNFUUVERVFIL3hBQWRBQUFCQkFNQkFRQUFBQUFBQUFBQUFBQUFBd1lIQ1FRRkNBSUIvOFFBUkJBQUFRUUJBd0VEQmcwQ0F3Y0ZBQUFBQWdFREJBVUdBQWNSRWdnVElSUVZNVFNCc1FrWElpTTFRVkZUZ3BHU3dkSVdNak5DWVJna09WSmljYUZEY25XMDhQL0VBQllCQVFFQkFBQUFBQUFBQUFBQUFBQUFBQUFCQS8vRUFCd1JBUUVBQWdNQkFRQUFBQUFBQUFBQUFBQUJBaEVESVRHQndmL2FBQXdEQVE='))
join_list = {
    "EAHZ2016": "黄正",
    "EACEM3JA": "陆成杰",
    "EAGW29U3": "李晗",
    "EA376WF9": "袁剑华",
    "EAYPM21L": "黎晃豪",
    "EAALLXXU": "姜清扬",
    "EA4PVIHH": "董艺涵",
    "EA9XZIPE": "刘骐华",
    "EAW8R6B5": "周任知",
    "EAC9NZWL": "黄静嘉",
    "EA7XSLGC": "饶骊文",
    "EAIFFASQ": "张钘晖",
    "EAN1YHEY": "邱炜基",
    "EA6W4B18": "王林杰",
    "EA9MKP33": "王桢荣",
    "EA1HT5UP": "刘倩妍",
    "EAPP0L7X": "陈吴刚",
    "EAQQSU95": "梁林",
    "EA3S1XWS": "王子轩",
    "EAMON91F": "曾源原",
    "EA0L3SMU": "朱粤锋",
    "EA8C6K1W": "叶朗钊",
    "EAUXMQSA": "安秋霖",
    "EA8MX18T": "陈柯瑜",
    "EAXS6S7Z": "林锦晖",
    "EA0R5SO7": "王彦哲",
    "EAZ764YU": "刘东明",
    "EAT32CKX": "林健",
    "EAKV5BJA": "黄烨基",
    "EA4O5Q3G": "祁俊东",
    "EAHHHGMX": "林家麒",
    "EA8X64HB": "许颀昊",
    "EA92RV9N": "孙朴凡",
    "EA46OU1F": "杨轩",
    "EALR63S2": "姚博耀",
    "EAMQAJAB": "冯兴鼎",
    "EAF6NVPT": "张梓荣",
    "EA8IF4DI": "刘雨鑫",
    "EA7N6NV9": "谭婉莹",
    "EABMDMAQ": "陈东平",
    "EA2ZZ622": "周睿星",
    "EAMWKE8L": "关浩林",
    "EA6HXDD4": "陈强",
    "EAONJTAI": "张梓豪",
    "EAM0D3B8": "肖岚沧",
    "EAY80U3X": "陆润中",
    "EA7BQCTL": "陈佳琦",
    "EAIUZ04M": "卢俊涛",
    "EASQT3BU": "余楚煜",
    "EA337F86": "丁智浩",
    "EAT3ETQC": "张静君",
    "EA5XJPE2": "罗煜耀",
    "EAH5RL0N": "陈俊玮",
    "EAAN0KUL": "许文渊",
    "EA8P2WOX": "郑正达",
    "EAWJMNDE": "彭斌",
    "EAXQ2KQM": "何政旗",
    "EAAOPZIO": "郑嘉璐",
    "EA1L32RY": "李阳林",
    "EAAJSHHK": "许文鑫",
    "EAHEMFT6": "安馨",
    "EAFNCV8I": "李鹏辉",
    "EANHUIAD": "杨丽敏",
    "EAHHPU7Y": "朱玲",
    "EAXZ5XAR": "杨欣锐",
    "EA1RYO2L": "陈天行",
    "EAD4F48E": "彭嘉栋",
    "EA6YJVBQ": "马洛恒"
}


@plugin_receiver.wx
def check_join_code(ctx: WeChatMsg):
    if ctx.IsGroup or len(ctx.Content) != 8:
        return

    if ctx.Content.startswith("EA") and len(join_list[ctx.Content]) > 0:
        join_real_name(ctx.FromUserName, join_list[ctx.Content])
        action.sendCdnImg(ctx.FromUserName, xml=pic_content)

    return
