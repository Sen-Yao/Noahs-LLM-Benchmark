from .task_1_spirit_in_the_bottle import SpiritInTheBottle
from .transaction_classify import TransactionClassify

# 将所有任务类放在一个列表中
ALL_TASKS = [
    SpiritInTheBottle(article_filename="SpiritInTheBottle.txt"),
    TransactionClassify(),
]