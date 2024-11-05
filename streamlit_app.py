import streamlit as st
import subprocess
import sys
import os

# 设置页面标题
st.title("社交媒体搜索工具 📱")

# 添加简单说明
st.markdown("""
这个工具可以帮助您搜索不同社交平台上的内容。
""")

# 创建选择平台的下拉菜单
platform = st.selectbox(
    "选择要搜索的平台",
    ["Twitter", "Instagram", "Facebook", "Reddit", "TikTok", "Medium", "Quora", "Pinterest"]
)

# 创建用户名输入框
username = st.text_input("请输入要搜索的用户名", "")

# 创建浏览器选择（对某些平台需要）
browser = st.selectbox(
    "选择浏览器",
    ["chrome", "firefox"]
)

# 创建搜索按钮
if st.button("开始搜索"):
    if username:
        st.info(f"正在搜索 {platform} 上的 '{username}'...")
        try:
            # 根据不同平台选择不同的脚本
            script_name = f"{platform.lower()}.py"
            # 执行搜索
            if platform in ["Pinterest", "Medium", "Twitter"]:
                command = f"python {script_name} {username}"
            else:
                command = f"python {script_name} {username} --browser {browser}"
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # 显示结果
            if result.stdout:
                st.success("搜索完成！")
                st.code(result.stdout)
            if result.stderr:
                st.error(result.stderr)
                
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
    else:
        st.warning("请输入用户名！")

# 添加页脚
st.markdown("---")
st.markdown("由 Python 社交媒体搜索工具提供支持 🚀")
