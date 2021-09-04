import base64
import os


in_f = open('./img.txt','rb')
out_f = open('./base64.decode.png','wb')
base64.decode(in_f,out_f)
in_f.close()
out_f.close()