# coding=UTF-8

"""
Created on 2016-7-11

@author: YRK

signature算法：
1、将所有非sign键的字典进行以键（string类型）反序排列，并以{key}{value}形式依次组装成字符串
2、将组装好的字符串进行sha1算法进行40长度字符串生成
3、通过参数数量决定获取抽样数量（默认抽样数量=参数数量*抽样因子（默认1.4）），并通过 签名长度 / 抽样次数 来决定间隔数量，通过抽样数量及间隔来决定抽取的字符串。

         如：
             原字典数据：{'auth_token':'1231kandfkk1sdf', 'timestamp':123154143123, 'method':'get_user', 'account':'test', 'passwd':'test'}
             生成字符串：timestamp123154143123passwdtestmethodget_userauth_token1231kandfkk1sdfaccounttest
             算法生成：114d8d89b3135639d75ed99144310274b7586299
             最终采样：1d19d47

     注：如果 默认抽样数量 > sha1算法计算的签名长度，则立即返回sha1算法计算的签名

     其他：
        参数是 3个，产生的密匙为：11d7
        参数是 4个，产生的密匙为：1bd4b
        参数是 5个，产生的密匙为：1d37905
        参数是 6个，产生的密匙为：1d19d478
        参数是 7个，产生的密匙为：18b679348
        参数是 8个，产生的密匙为：1d9135942b6
        参数是 9个，产生的密匙为：1d816dd13776
        参数是 10个，产生的密匙为：14db337d940452
        参数是 11个，产生的密匙为：14db16d59432b52
        参数是 12个，产生的密匙为：14d91597d9417b82
        参数是 13个，产生的密匙为：1488b3697d94304782
        参数是 14个，产生的密匙为：1488b153d5914124782
        参数是 15个，产生的密匙为：11dd933697ed94307b569
        参数是 16个，产生的密匙为：11dd93153d5d914127b569
        参数是 17个，产生的密匙为：11dd8b15697ed9431247569
        参数是 18个，产生的密匙为：11d88b3353d7ed944107b7869
        参数是 19个，产生的密匙为：11d88931569d5d9143127b7869
        参数是 20个，产生的密匙为：1148d9b1353975d99441074b5829
        参数是 21个，产生的密匙为：1148d8b33569d7ed9143107475829
        参数是 22个，产生的密匙为：1148d8b31563d75d99443027b75629
        参数是 23个，产生的密匙为：114dd89b13569d75d991431074b78629
        参数是 24个，产生的密匙为：114d889b315639d5ed914431274b78629
        参数是 25个，产生的密匙为：114d8d8b313563d75ed994431027b758629
        参数是 26个，产生的密匙为：114d8d89b135639d75d9914431074b758629
        参数是 27个，产生的密匙为：114d8d89b313539d75ed9914410274b758629
        参数是 28个，产生的密匙为：114d8d89b3135639d75ed99144310274b758629
        参数是 29个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 30个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 31个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 32个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 33个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 34个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 35个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 36个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 37个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 38个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 39个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 40个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 41个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 42个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 43个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299
        参数是 44个，产生的密匙为：114d8d89b3135639d75ed99144310274b7586299

"""

import hashlib

def unique_parms(parms, sign_key = "sign"):
    parm_list = [ '{key}{val}'.format(key = key, val = parms[key]) \
                 for key in sorted(parms.keys(), reverse = True) if key != sign_key]
    return ''.join(parm_list), len(parm_list)

def generate_signature(string, interval, divisor = 1.4):
    string = string.encode('utf-8')
    sign_string = hashlib.sha1(string).hexdigest()
    sign_string_len = len(sign_string)
    sample_count = int(interval * divisor)
    if sample_count >= sign_string_len :
        return sign_string
#     elif sample_count == 0:
#         # 当没有任何参数，暂定返回所有sign_string,理论上这个操作不存在
#         return sign_string
    cycle = int(sign_string_len / sample_count)
    return ''.join(sign_string[index * cycle] for index in range(sample_count))


if __name__ == "__main__":
    parms = {'auth_token':'1231kandfkk1sdf', 'timestamp':123154143123, 'sign':123123123123, 'method':'get_user', 'account':'test', 'passwd':'test'}
    unique_string , length = unique_parms(parms)
    print(unique_string)
    print(generate_signature(unique_string, length))
    for index in range(3, 45, 1):
        print("参数是 {}个，产生的密匙为：{}".format(index, generate_signature(unique_string, index)))
        if index % 5 == 0 :
            print
