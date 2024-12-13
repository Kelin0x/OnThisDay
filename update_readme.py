import requests
from datetime import datetime
import json
import sys

def get_today_in_history():
    try:
        url = "https://history.muffinlabs.com/date"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        events = data['data']['Events'][-5:]  # 获取最近5条历史事件
        formatted_events = []
        for event in events:
            formatted_events.append(f"- {event['year']}年：{event['text']}")
        
        return formatted_events
    except Exception as e:
        print(f"获取历史数据时出错: {str(e)}")
        sys.exit(1)

def update_readme():
    try:
        # 读取 README.md 文件
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 获取历史事件
        events = get_today_in_history()
        
        # 准备新的内容
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_content = f"\n> 更新时间：{update_time}\n\n"
        for event in events:
            new_content += f"{event}\n"
            
        # 在标记之间更新内容
        start_marker = "## 📖 今日历史"
        end_marker = "## 🛠️ 技术实现"
        
        # 查找开始和结束位置
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker)
        
        if start_pos == -1 or end_pos == -1:
            print("未找到更新区域标记")
            sys.exit(1)
            
        # 组合新的 README 内容
        new_readme = (
            content[:start_pos] +
            start_marker +
            new_content +
            "\n" +
            content[end_pos:]
        )
            
        # 写入更新后的内容
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(new_readme)
            
    except Exception as e:
        print(f"更新 README 时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    update_readme() 