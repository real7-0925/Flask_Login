#abort message

import sys
import traceback

def abort_msg(e):
    #引發錯誤的class
    error_class = e.__class__.__name__
    
    #得到詳細訊息
    detail = e.args[0]

    #得到錯誤的完整資訊 Casll Stack
    cl, exc, tb = sys.exc_info()
    
    #取得最後一行的錯誤訊息
    lastCallStack = traceback.extract_tb(tb)[-1]

    #錯誤的檔案位置名稱
    fileName = lastCallStack[0]

    #錯誤行數
    lineNum = lastCallStack[1]

    #錯誤Function名稱
    funcName = lastCallStack[2]

    #產生錯誤訊息
    errMsg = {error_class: [detail]}
    return errMsg