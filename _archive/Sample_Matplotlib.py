#!/usr/bin/env python
# coding: utf-8
#from matplotlib import backends
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from PIL import Image
import pylab

custom_font = mpl.font_manager.FontProperties(fname='C:\\Anaconda\\Lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\huawenxihei.ttf')
# 必须配置中文字体，否则会显示成方块
# 所有希望图表显示的中文必须为unicode格式,为方便起见我们将字体文件重命名为拼音形式 custom_font表示自定义字体

font_size = 10 # 字体大小
fig_size = (8, 6) # 图表大小

names = (u'小刚', u'小芳') # 姓名元组
subjects = (u'物理', u'化学', u'生物') # 学科元组
scores = ((65, 80, 72), (75, 90, 85)) # 成绩元组


mpl.rcParams['font.size'] = font_size   # 更改默认更新字体大小
mpl.rcParams['figure.figsize'] = fig_size   # 修改默认更新图表大小
bar_width = 0.35   # 设置柱形图宽度

index = np.arange(len(scores[0]))

# 绘制“小明”的成绩 index表示柱形图左边x的坐标
rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])
# 绘制“小红”的成绩
rects2 = plt.bar(index + bar_width, scores[1], bar_width, color='#ED1C24', label=names[1])

plt.xticks(index + bar_width, subjects, fontproperties=custom_font)        # X轴标题
plt.ylim(ymax=100, ymin=0)        # Y轴范围

plt.title(u'彩虹班同学成绩对比', fontproperties=custom_font)     # 图表标题

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=2, prop=custom_font)
# 图例显示在图表下方 似乎左就是右，右就是左，上就是下，下就是上，center就是center
# bbox_to_anchor左下角的位置？ ncol就是numbers of column默认为1


# 添加数据标签 就是矩形上面的成绩数字
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # horizontalalignment='center' plt.text(x坐标，y坐标，text,位置)
        # 柱形图边缘用白色填充，为了更加清晰可分辨
        rect.set_edgecolor('white')

add_labels(rects1)
add_labels(rects2)


plt.savefig('scores_par.png')   # 图表输出到本地
#pylab.imshow('scores_par.png')
pylab.show('scores_par.png')    # 并打印显示图片