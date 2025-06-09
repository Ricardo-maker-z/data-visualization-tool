import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False     # 用来正常显示负号

# 设置页面标题
st.title("数据可视化工具")

# 文件上传
uploaded_file = st.file_uploader("选择数据文件", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 读取文件
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 显示数据预览
        st.subheader("数据预览")
        st.dataframe(df.head())
        
        # 选择图表类型
        chart_type = st.selectbox(
            "选择图表类型",
            ["柱状图", "折线图", "散点图", "饼图"]
        )
        
        # 根据图表类型选择不同的参数
        if chart_type in ["柱状图", "折线图", "散点图"]:
            x_column = st.selectbox("选择X轴数据列", df.columns.tolist())
            y_column = st.selectbox("选择Y轴数据列", df.select_dtypes(include=['number']).columns.tolist())
            
            # 排序选项
            enable_sort = st.checkbox("启用数据排序")
            if enable_sort:
                sort_direction = st.radio("排序方向", ["升序", "降序"])
                
            # 图表标题
            chart_title = st.text_input("图表标题", f"{y_column} 与 {x_column} 的关系")
            
            # 生成图表
            if st.button("生成图表"):
                # 准备数据
                plot_df = df.copy()
                if enable_sort:
                    plot_df = plot_df.sort_values(by=y_column, 
                                                ascending=(sort_direction == "升序"))
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if chart_type == "柱状图":
                    sns.barplot(data=plot_df, x=x_column, y=y_column, ax=ax)
                elif chart_type == "折线图":
                    sns.lineplot(data=plot_df, x=x_column, y=y_column, ax=ax)
                else:  # 散点图
                    sns.scatterplot(data=plot_df, x=x_column, y=y_column, ax=ax)
                
                ax.set_title(chart_title)
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # 显示图表
                st.pyplot(fig)
                
                # 提供下载选项
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                st.download_button(
                    label="下载图表",
                    data=buf.getvalue(),
                    file_name=f"{chart_title}.png",
                    mime="image/png"
                )
        
        elif chart_type == "饼图":
            value_column = st.selectbox("选择数值列", df.select_dtypes(include=['number']).columns.tolist())
            category_column = st.selectbox("选择分类列", df.columns.tolist())
            
            # 排序选项
            enable_sort = st.checkbox("启用数据排序")
            if enable_sort:
                sort_direction = st.radio("排序方向", ["升序", "降序"])
            
            chart_title = st.text_input("图表标题", f"{category_column}的{value_column}分布")
            
            if st.button("生成图表"):
                # 准备饼图数据
                pie_data = df.groupby(category_column)[value_column].sum()
                
                # 排序数据
                if enable_sort:
                    pie_data = pie_data.sort_values(ascending=(sort_direction == "升序"))
                
                # 创建饼图
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
                ax.set_title(chart_title)
                plt.tight_layout()
                
                # 显示图表
                st.pyplot(fig)
                
                # 提供下载选项
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                st.download_button(
                    label="下载图表",
                    data=buf.getvalue(),
                    file_name=f"{chart_title}.png",
                    mime="image/png"
                )
    
    except Exception as e:
        st.error(f"处理文件时出错: {str(e)}")
else:
    st.info("请上传CSV或Excel文件以开始数据可视化")