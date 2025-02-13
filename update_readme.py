import requests
from datetime import datetime
import json
import sys
import pytz
from urllib.parse import quote

def get_today_events(lang='zh'):
    """获取维基百科历史事件（支持中英文）"""
    endpoint = {
        'zh': 'https://zh.wikipedia.org/api/rest_v1/feed/onthisday/events',
        'en': 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events'
    }

    try:
        # 获取当前月份和日期
        beijing_tz = pytz.timezone('Asia/Shanghai')
        today = datetime.now(beijing_tz)
        mmdd = f"{today.month}/{today.day}"

        # 使用媒体基金会API
        url = f"{endpoint[lang]}/{mmdd}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) README-Updater/1.0',
            'Api-User-Agent': 'muffin-history-bot/1.0 (contact@example.com)'
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json().get('events', [])[:10]  # 取前10条

    except requests.exceptions.SSLError as e:
        # 添加证书验证异常处理
        print(f"SSL证书验证失败: {str(e)}")
        return None
    except Exception as e:
        print(f"API请求异常: {str(e)}")
        return None

def format_wiki_events(events, max_items=5):
    """处理维基百科数据结构"""
    formatted = []
    seen = set()

    for event in events:
        try:
            year = event.get('year', '')
            text = event.get('text', '').split('（来源：')[0]  # 移除来源信息
            
            # 中文版处理
            if 'pages' in event:
                text = event['pages'][0].get('normalizedtitle', text)
            
            # 去重关键字段
            key = f"{year}-{text[:20]}"
            if key not in seen and year.isdigit():
                seen.add(key)
                formatted.append(f"- {year}年：{text}")
                if len(formatted) >= max_items:
                    break
        except:
            continue
            
    return formatted if len(formatted) > 0 else ["- 暂未获取到历史数据"]

def update_readme():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    update_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # 获取数据（优先中文，失败时用英文）
    events = get_today_events('zh') or get_today_events('en')
    formatted = format_wiki_events(events) if events else []
    
    # 更新文件逻辑（保持原有部分不变）...
    # （此处可沿用原来的文件更新模块）

if __name__ == "__main__":
    update_readme()
