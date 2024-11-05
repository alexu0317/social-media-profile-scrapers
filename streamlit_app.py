import streamlit as st
import subprocess
import sys
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

# 显示当前工作环境（调试用）
st.sidebar.markdown("### 调试信息")
st.sidebar.write("当前目录:", os.getcwd())
st.sidebar.write("目录内容:", os.listdir())

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
            st.sidebar.write(f"寻找脚本: {script_path}")
            st.sidebar.write(f"脚本存在?: {script_path.exists()}")
            
            # 构建命令
            if platform in ["Pinterest", "Medium", "Twitter"]:
                command = f"python {platform.lower()}.py {username}"
            else:
                command = f"python {platform.lower()}.py {username} --browser {browser}"
            
            st.sidebar.write("执行命令:", command)
            
            # 执行搜索命令
            try:
                # 先检查文件是否存在
                if not script_path.exists():
                    st.error(f"找不到所需的脚本文件: {script_path}")
                    st.info("请确保所有必要的文件都已正确部署")
                else:
                    # 执行命令
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    
                    # 显示结果
                    if result.stdout:
                        st.success("搜索完成！")
                        try:
                            # 尝试解析 JSON 结果
                            data = json.loads(result.stdout)
                            st.json(data)
                        except json.JSONDecodeError:
                            st.text_area("搜索结果", result.stdout, height=300)
                    
                    # 显示错误信息（如果有）
                    if result.stderr:
                        st.error("执行过程中遇到以下问题：")
                        st.code(result.stderr)
                
            except Exception as e:
                st.error(f"执行命令时出错: {str(e)}")
                st.code(traceback.format_exc())
                
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    else:
        st.warning("请输入用户名！")

# 添加页脚
st.markdown("---")
st.markdown("💡 由 Python 社交媒体搜索工具提供支持")

# 添加调试信息开关
if st.sidebar.checkbox("显示详细调试信息"):
    st.sidebar.write("Python 版本:", sys.version)
    st.sidebar.write("系统平台:", sys.platform)
    st.sidebar.write("环境变量:", dict(os.environ))
