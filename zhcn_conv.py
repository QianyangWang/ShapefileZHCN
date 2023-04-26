import time
import zhconv
import dbf
import glob
import os.path


def conv_shp(file_path):
  tb = dbf.Table(file_path)
  try:
    print("尝试使用默认编码转换文件【{}】".format(file_path))

    titles = dbf.get_fields(file_path)
    # print(titles)

    tb.open(mode=dbf.READ_WRITE)
    for record in tb:
      with record as r:
        for v in titles:

          if isinstance(record[v],str):
            try:
              record[v] = zhconv.convert(record[v], 'zh-cn')
            except:
              print("记录【{}】转换不成功".format(record[v].replace(" ","")))
              #print("记录【{}】转换不成功".format(record[v]))

    tb.close()
    print("{}繁简转换完成！".format(file_path))
  except:
    print("文件【{}】默认编码转换失败，尝试使用utf8转换".format(file_path))
    tb.close()
    tb = dbf.Table(file_path,codepage="utf8")
    titles = dbf.get_fields(file_path)
    # print(titles)

    tb.open(mode=dbf.READ_WRITE)
    for record in tb:
      with record as r:
        for v in titles:

          if isinstance(record[v], str):
            try:
              record[v] = zhconv.convert(record[v], 'zh-cn')
            except:
              print("记录【{}】转换不成功".format(record[v].replace(" ", "")))
              # print("记录【{}】转换不成功".format(record[v]))

    tb.close()
    print("{}繁简转换完成！".format(file_path))
  try:
    tb.close()
  except:
    pass

def check_file(val):
  if os.path.isfile(val):
    return 0
  elif os.path.isdir(val):
    return 1
  else:
    return -1

def dbf_name(val):
  name = os.path.splitext(val)[0]
  dbf_name = name+".dbf"
  return dbf_name


if __name__ == "__main__":

  val = input("请输入文件路径或文件夹，输入0退出：")
  if val == "0":
    exit(0)
  else:
    check = check_file(val)
    if check == 0:
      f_path = dbf_name(val)
      conv_shp(f_path)
    elif check == 1:
      f_list = glob.glob("{}\*.dbf".format(val))
      for f in f_list:
        conv_shp(f)
    else:
      print("转换失败，输入内容非文件/路径")

    time.sleep(2)


