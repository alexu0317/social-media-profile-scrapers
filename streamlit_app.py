import streamlit as st
import subprocess
import sys
import os
import json
from pathlib import Path

# 设置页面标题和说明
st.set_page_config(page_title="社交媒体搜索工具", layout="wide")
st.title("社交媒体搜索工具 📱")

st.markdown("""
这个工具可以帮助您搜索不同社交平台上的内容。
""")

# 检查必要的Python文件是否存在
def check_files():
    required_files = ['facebook.py', 'twitter.py', 'instagram.py']
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    return missing_files

# 创建选择平台的下拉菜单
platform = st.selectbox(
    "选择要搜索的平台",
    ["Twitter", "Facebook", "Instagram", "Reddit", "TikTok", "Medium", "Quora", "Pinterest"]
)

# 创建用户名输入框
username = st.text_input("请输入要搜索的用户名")

# 创建浏览器选择框
browser = st.selectbox(
    "选择浏览器",
    ["chrome", "firefox"]
)

# 当点击搜索按钮时
if st.button("开始搜索"):
    if username:
        # 检查文件是否存在
        missing_files = check_files()
        if missing_files:
            st.error(f"缺少必要的文件: {', '.join(missing_files)}")
        else:
            try:
                st.info(f"正在搜索 {platform} 上的 '{username}'...")
                
                # 根据不同平台选择不同的脚本
                script_name = f"{platform.lower()}.py"
                
                # 设置命令
                if platform in ["Pinterest", "Medium", "Twitter"]:
                    command = f"python {script_name} {username}"
                else:
                    command = f"python {script_name} {username} --browser {browser}"
                
                # 执行命令
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    # 显示结果
                    if result.stdout:
                        st.success("搜索完成！")
                        try:
                            # 尝试解析JSON结果
                            data = json.loads(result.stdout)
                            st.json(data)
                        except json.JSONDecodeError:
                            # 如果不是JSON格式，直接显示文本
                            st.text(result.stdout)
                    
                    # 如果有错误信息，显示出来
                    if result.stderr:
                        st.error(f"搜索过程中出现错误: {result.stderr}")
                
                except Exception as e:
                    st.error(f"执行命令时出错: {str(e)}")
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
    else:
        st.warning("请输入用户名！")

# 添加页脚
st.markdown("---")
st.markdown("由 Python 社交媒体搜索工具提供支持 🚀")
