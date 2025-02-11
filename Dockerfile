# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install -r requirements.txt

# 复制应用代码
COPY main.py .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "main.py"]