import requests
from datetime import datetime
import json
import sys

def get_today_in_history():
    try:
        url = "https://history.muffinlabs.com/date"
        response = requests.get(url, timeout=10)  # 添加超时设置
        response.raise_for_status()  # 检查响应状态
        data = response.json()
        
        events = data['data']['Events'][-5:]
        formatted_events = []
        for event in events:
            formatted_events.append(f"- {event['year']}年：{event['text']}")
        
        return formatted_events
    except Exception as e:
        print(f"获取历史数据时出错: {str(e)}")
        sys.exit(1)

def update_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.readlines()
        
        events = get_today_in_history()
        
        new_content = []
        found_section = False
        for line in content:
            new_content.append(line)
            if '## 📅 历史上的今天' in line:
                found_section = True
                new_content.append('\n')
                new_content.append(f'> 更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
                for event in events:
                    new_content.append(f'{event}\n')
                break
        
        if not found_section:
            print("未找到更新区域标记")
            sys.exit(1)
            
        with open('README.md', 'w', encoding='utf-8') as file:
            file.writelines(new_content)
            
    except Exception as e:
        print(f"更新 README 时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    update_readme() 