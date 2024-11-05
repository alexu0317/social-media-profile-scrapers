import streamlit as st
import os
import json
from pathlib import Path

# 设置页面和标题
st.set_page_config(page_title="社交媒体搜索工具", layout="wide")
st.title("社交媒体搜索工具 📱")

# 显示使用说明
st.markdown("""
### 使用说明 📖
1. 选择要搜索的社交媒体平台
2. 输入要搜索的用户名
3. 选择浏览器（使用默认设置即可）
""")

# 创建选择平台的下拉菜单
platform = st.selectbox(
    "选择要搜索的平台",
    ["Twitter", "Facebook", "Instagram", "Reddit", "TikTok", "Medium", "Quora", "Pinterest"]
)

# 创建用户名输入框
username = st.text_input("请输入要搜索的用户名")

# 创建浏览器选择框
browser = st.selectbox(
    "选择浏览器（可使用默认设置）",
    ["chrome", "firefox"]
)

# 当点击搜索按钮时
if st.button("开始搜索 🔍"):
    if username:
        try:
            st.info(f"正在搜索 {platform} 上的 '{username}'...")
            
            # 获取脚本路径
            script_path = Path(f"{platform.lower()}.py")
            
            # 构建命令
            if platform in ["Pinterest", "Medium", "Twitter"]:
                os.system(f"python {platform.lower()}.py {username}")
            else:
                os.system(f"python {platform.lower()}.py {username} --browser {browser}")
            
            st.success("搜索完成！")
                
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
    else:
        st.warning("请输入用户名！")

# 添加页脚
st.markdown("---")
st.markdown("💡 由 Python 社交媒体搜索工具提供支持")
