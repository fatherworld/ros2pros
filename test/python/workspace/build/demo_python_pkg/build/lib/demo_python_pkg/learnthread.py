import threading
import requests
class Download:
    def download(self,url,callback):
        print(f'线程:{threading.get_ident} 开始下载： {url}')
        response=requests.get(url)
        response.encoding='utf-8'
        callback(url,response.text)
    def start_download(self,url,callback):
        thread=threading.Thread(target=self.download,args=(url,callback))
        thread.start()
    
def download_finish_callback(url,result):
    print(f'{url} 下载完成，一共{len(result)}个字节,内容是{result}')

def main():
    urls = ["http://localhost:8000/novel1.txt","http://localhost:8000/novel2.txt","http://localhost:8000/novel3.txt"]
    for iurl in urls:
        d = Download()
        d.start_download(iurl,download_finish_callback)