#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童哲学对话数据整合脚本
将四个Excel文件合并为一个文件，并重新排列第一列的标号顺序
"""

import pandas as pd
import os
from pathlib import Path

def merge_excel_files():
    """
    合并四个Excel文件并重新编号
    """
    # 定义文件路径
    data_dir = Path("initial_data")
    
    # 检查目录是否存在
    if not data_dir.exists():
        print(f"错误：目录 {data_dir} 不存在")
        return
    
    # 定义要合并的文件列表
    excel_files = [
        "儿童哲学对话数据1.xlsx",
        "儿童哲学对话数据2.xlsx", 
        "儿童哲学对话数据3.xlsx",
        "儿童哲学对话数据4.xlsx"
    ]
    
    # 存储所有数据的列表
    all_data = []
    
    print("开始读取Excel文件...")
    
    # 逐个读取Excel文件
    for i, filename in enumerate(excel_files, 1):
        file_path = data_dir / filename
        
        if not file_path.exists():
            print(f"警告：文件 {filename} 不存在，跳过")
            continue
            
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            print(f"成功读取 {filename}，包含 {len(df)} 行数据")
            
            # 将数据添加到列表中
            all_data.append(df)
            
        except Exception as e:
            print(f"读取文件 {filename} 时出错：{e}")
            continue
    
    if not all_data:
        print("错误：没有成功读取任何文件")
        return
    
    print(f"\n成功读取 {len(all_data)} 个文件")
    
    # 合并所有数据
    print("正在合并数据...")
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # 重新分配session_id：当turn_id从大变小时表示新对话开始
    print("重新分配session_id（基于turn_id变化）...")
    session_counter = 1
    merged_df.iloc[0, 0] = session_counter  # 第一行的session_id设为1
    
    for i in range(1, len(merged_df)):
        current_turn_id = merged_df.iloc[i]['turn_id']
        previous_turn_id = merged_df.iloc[i-1]['turn_id']
        
        # 如果当前turn_id小于前一个turn_id，说明开始了新的对话
        if current_turn_id < previous_turn_id:
            session_counter += 1
        
        merged_df.iloc[i, 0] = session_counter  # 第一列是session_id
    
    # 生成输出文件名
    output_filename = "儿童哲学对话数据_合并版.xlsx"
    
    try:
        # 保存合并后的数据
        print(f"正在保存到 {output_filename}...")
        merged_df.to_excel(output_filename, index=False)
             
    except Exception as e:
        print(f"保存文件时出错：{e}")

def main():
    """
    主函数
    """
    print("=" * 50)
    print("儿童哲学对话数据整合工具")
    print("=" * 50)
       
    # 执行合并操作
    merge_excel_files()

if __name__ == "__main__":
    main()