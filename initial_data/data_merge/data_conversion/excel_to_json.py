#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童哲学对话数据转换脚本
将合并后的Excel数据转换为JSONL格式，用于AI训练
"""

import pandas as pd
import json
from pathlib import Path

def convert_excel_to_jsonl():
    """
    将Excel数据转换为JSONL格式
    """
    input_file = Path("../儿童哲学对话数据_合并版.xlsx")
    
    if not input_file.exists():
        return
    
    df = pd.read_excel(input_file)
    grouped = df.groupby('session_id')
    conversations = []
    
    for session_id, group in grouped:
        group_sorted = group.sort_values('turn_id')
        messages = []
        
        for _, row in group_sorted.iterrows():
            message = {
                "role": row['role'],
                "content": str(row['content']).strip()
            }
            messages.append(message)
        
        conversation = {"messages": messages}
        conversations.append(conversation)
    
    output_file = "儿童哲学对话数据.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for conversation in conversations:
            json_line = json.dumps(conversation, ensure_ascii=False)
            f.write(json_line + '\n')

def main():
    convert_excel_to_jsonl()

if __name__ == "__main__":
    main()