"""
生产者
消费者
    celery -A proj worker -l INFO

     在虚拟环境下执行指令
     celery -A celery 实例的脚本路径， worker -l INFO
队列（中间人，经纪人）
    设置 broker
    redis
Celery  --  将这3者都实现了
    0 为celery，设置 Django 环境

    1. 创建 celery 实例
"""

# 0. 为celery的运行，设置Django的环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')
# 1. 创建celery实例
from celery import Celery
# 参数1： main 设置脚本路径就可以了; 脚本路径是唯一的
app = Celery('celery_tasks')

# 2. 设置 broker
# 我们通过加载配置文件来设置broker
app.config_from_object('celery_tasks.config')

# 3. 需要 celery 自动检测指定包的任务
# autodiscover_tasks 参数是列表
# 列表中的元素是 tasks的路径
app.autodiscover_tasks(['celery_tasks.sms'])
