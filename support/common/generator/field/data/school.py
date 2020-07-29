# coding=UTF-8

SHOOL_LIST = [
    ["北京大学", "世界一流大学", "北京", "北京"],
    ["清华大学", "世界一流大学", "北京", "北京"],
    ["复旦大学", "世界一流大学", "上海", "上海"],
    ["浙江大学", "世界一流大学", "浙江", "杭州"],
    ["南京大学", "世界一流大学", "江苏", "南京"],
    ["上海交通大学", "世界一流大学", "上海", "上海"],
    ["华中科技大学", "世界知名高水平大学", "湖北", "武汉"],
    ["中国科学技术大学", "世界一流大学", "安徽", "合肥"],
    ["中国人民大学", "世界一流大学", "北京", "北京"],
    ["天津大学", "世界知名高水平大学", "天津", "天津"],
    ["武汉大学", "世界知名高水平大学", "湖北", "武汉"],
    ["南开大学", "世界知名高水平大学", "天津", "天津"],
    ["山东大学", "世界知名高水平大学", "山东", "济南"],
    ["中山大学", "世界知名高水平大学", "广东", "北京"],
    ["西安交通大学", "世界知名高水平大学", "山西", "西安"],
    ["哈尔滨工业大学", "世界知名高水平大学", "黑龙江", "哈尔滨"],
    ["东南大学", "世界知名高水平大学", "江苏", "南京"],
    ["四川大学", "世界知名高水平大学", "四川", "成都"],
    ["吉林大学", "世界知名高水平大学", "吉林", "长春"],
    ["同济大学", "世界知名高水平大学", "上海", "上海"],
    ["北京航空航天大学", "世界知名高水平大学", "北京", "北京"],
    ["北京师范大学", "世界知名高水平大学", "北京", "北京"],
    ["厦门大学", "世界知名高水平大学", "福建", "厦门"],
    ["西北工业大学", "世界高水平大学", "陕西", "西安"],
    ["中南大学", "世界知名高水平大学", "湖南", "长沙"],
    ["东北大学", "世界高水平大学", "辽宁", "沈阳"],
    ["大连理工大学", "世界高水平大学", "辽宁", "大连"],
    ["湖南大学", "世界高水平大学", "湖南", "长沙"],
    ["华南理工大学", "世界高水平大学", "广东", "广州"],
    ["北京理工大学", "世界高水平大学", "北京", "北京"],
    ["兰州大学", "世界高水平大学", "甘肃", "兰州"],
    ["华东师范大学", "世界高水平大学", "上海", "上海"],
    ["中国农业大学", "世界高水平大学", "北京", "北京"],
    ["电子科技大学", "世界高水平大学", "四川", "成都"],
    ["重庆大学", "世界高水平大学", "重庆", "重庆"],
    ["华中农业大学", "世界高水平大学", "湖北", "武汉"],
    ["河海大学", "世界高水平大学", "江苏", "南京"],
    ["南京农业大学", "中国一流大学", "江苏", "南京"],
    ["华中师范大学", "中国一流大学", "湖北", "武汉"],
    ["郑州大学", "中国一流大学", "河南", "郑州"],
    ["中国海洋大学", "世界高水平大学", "山东", "青岛"],
    ["西安电子科技大学", "中国一流大学", "陕西", "西安"],
    ["北京科技大学", "中国一流大学", "北京", "北京"],
    ["南京理工大学", "世界一流大学", "江苏", "南京"],
    ["北京交通大学", "中国一流大学", "北京", "北京"],
    ["华东理工大学", "中国一流大学", "上海", "上海"],
    ["北京邮电大学", "世界高水平大学", "北京", "北京"],
    ["合肥工业大学", "中国一流大学", "安徽", "合肥"],
    ["南昌大学", "中国一流大学", "江西", "南昌"],
    ["北京协和医学院", "世界高水平大学", "北京", "北京"],
    ["南京航空航天大学", "中国一流大学", "江苏", "南京"],
    ["武汉理工大学", "中国一流大学", "湖北", "武汉"],
    ["西南交通大学", "中国一流大学", "四川", "成都"],
    ["暨南大学", "中国一流大学", "广东", "广州"],
    ["西南大学", "中国一流大学", "重庆", "重庆"],
    ["西北农林科技大学", "中国一流大学", "陕西", "咸阳"],
    ["东华大学", "中国一流大学", "上海", "上海"],
    ["西北大学", "中国一流大学", "陕西", "西安"],
    ["中南财经政法大学", "世界高水平大学", "湖北", "武汉"],
    ["苏州大学", "中国一流大学", "江苏", "苏州"],
    ["中国政法大学", "世界高水平大学", "北京", "北京"],
    ["北京化工大学", "中国一流大学", "北京", "北京"],
    ["昆明理工大学", "中国一流大学", "云南", "昆明"],
    ["南京师范大学", "中国一流大学", "江苏", "南京"],
    ["上海财经大学", "中国高水平大学", "上海", "上海"],
    ["湖南师范大学", "中国一流大学", "湖南", "长沙"],
    ["中国传媒大学", "世界高水平大学", "北京", "北京"],
    ["云南大学", "中国一流大学", "云南", "昆明"],
    ["上海大学", "中国高水平大学", "上海", "上海"],
    ["哈尔滨工程大学", "中国一流大学", "黑龙江", "哈尔滨"],
    ["福州大学", "中国高水平大学", "福建", "福州"],
    ["河南大学", "中国高水平大学", "河南", "开封"],
    ["华南农业大学", "中国一流大学", "广东", "广州"],
    ["东北师范大学", "中国一流大学", "吉林", "长春"],
    ["北京工业大学", "中国高水平大学", "北京", "北京"],
    ["中国地质大学", "世界高水平大学", "湖北", "武汉"],
    ["华南师范大学", "中国一流大学", "广东", "广州"],
    ["宁波大学", "中国高水平大学", "浙江", "宁波"],
    ["燕山大学", "中国一流大学", "河北", "秦皇岛"],
    ["中国石油大学", "中国一流大学", "北京", "北京"],
    ["太原理工大学", "中国一流大学", "山西", "太原"],
    ["上海理工大学", "中国高水平大学", "上海", "上海"],
    ["中国矿业大学", "世界高水平大学", "江苏", "徐州"],
    ["陕西师范大学", "中国一流大学", "陕西", "西安"],
    ["江南大学", "中国一流大学", "江苏", "江南"],
    ["首都师范大学", "中国高水平大学", "北京", "北京"],
    ["浙江工业大学", "中国高水平大学", "浙江", "杭州"],
    ["中国石油大学", "世界高水平大学", "北京", "北京"],
    ["北京中医药大学", "世界高水平大学", "北京", "北京"],
    ["浙江师范大学", "中国高水平大学", "浙江", "金华"],
    ["河北大学", "中国高水平大学", "河北", "保定"],
    ["对外经济贸易大学", "中国一流大学", "北京", "北京"],
    ["扬州大学", "中国高水平大学", "江苏", "扬州"],
    ["北京外国语大学", "世界高水平大学", "北京", "北京"],
    ["江苏大学", "中国高水平大学", "江苏", "镇江"],
    ["杭州电子科技大学", "中国高水平大学", "浙江", "杭州"],
    ["辽宁大学", "中国高水平大学", "辽宁", "沈阳"],
    ["中央民族大学", "世界高水平大学", "北京", "北京"],
    ["山西大学", "中国高水平大学", "山西", "太原"],
    ["南京工业大学", "中国高水平大学", "江苏", "南京"],
    ["西方医科大学", "中国高水平大学", "广东", "东莞"],
    ["齐鲁工业大学", "中国高水平大学", "山东", "济南"],
    ["广东工业大学", "中国高水平大学", "广东", "广州"],
    ["河南科技大学", "中国高水平大学", "河南", "洛阳"],
    ["山东师范大学", "中国高水平大学", "山东", "济南"],
    ["河北工业大学", "中国高水平大学", "天津", "天津"],
    ["成都理工大学", "中国高水平大学", "四川", "成都"],
    ["武汉科技大学", "中国高水平大学", "湖北", "武汉"],
]