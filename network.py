import requests
from loguru import logger
import datetime
import time
import os
import zipfile
from PySide6.QtCore import (QThread, QWaitCondition, QMutex, Signal, QMutexLocker)

class Update(QThread):
    valueChange = Signal(int)
    phaseChange = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.is_paused = bool(0)  # 标记线程是否暂停
        self.progress_value = int(0)  # 进度值
        self.mutex = QMutex()  # 互斥锁，用于线程同步
        self.cond = QWaitCondition()  # 等待条件，用于线程暂停和恢复
        self.tag= "latest"
        self.phase = "ready"

    def pause_thread(self):
        with QMutexLocker(self.mutex):
            self.is_paused = True  # 设置线程为暂停状态

    def resume_thread(self):
        if self.is_paused:
            with QMutexLocker(self.mutex):
                self.is_paused = False  # 设置线程为非暂停状态
                self.cond.wakeOne()  # 唤醒一个等待的线程

    def run(self):
        with QMutexLocker(self.mutex):
            while self.is_paused:
                self.cond.wait(self.mutex)  # 当线程暂停时，等待条件满足
            if self.progress_value >= 100 and self.phase=="complete":
                self.progress_value = 0
                self.phase = "ready"
                return  # 当进度值达到 100 时，重置为 0 并退出线程
            try:
                if os.name != 'nt':
                    url = self.getDownloadUrl("NamePickerOrg","NamePicker",self.tag)[0]
                else:
                    url = self.getDownloadUrl("NamePickerOrg","NamePicker",self.tag)[1]
                file_name = "proto.zip"
                size = 0
                with requests.get(url, stream=True,verify=False) as r:
                    total = int(r.headers["content-length"])
                    if r.status_code == 200:
                        with open(file_name, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                                    size += len(chunk)
                                    self.progress_value = (size/total)*100
                                    self.valueChange.emit(self.progress_value)
                                else:
                                    break
                            self.phase = "extract"
                            self.phaseChange.emit(self.phase)
                            logger.debug("Download complete")
                    else:
                        logger.error("错误：%d"%r.status_code)
                        self.phase = "error"
                        self.phaseChange.emit(self.phase)
                        return
                zip = zipfile.ZipFile(file_name)
                zip.extractall()
                zip.close()
                logger.info("Extract Complete")
                self.phase = "complete"
                self.phaseChange.emit(self.phase)
            except Exception as e:
                logger.error(f"错误: {e}")
                self.phase = "error"
                self.phaseChange.emit(self.phase)

    def getDownloadUrl(self,user:str,repo:str,reltag:str) -> list | None:
        try:
            self.phase = "get"
            self.phaseChange.emit(self.phase)
            url = f"https://api.github.com/repos/{user}/{repo}/releases/tags/{reltag}"
            logger.debug(url)
            response = requests.get(url,verify=False)
            asset_url = []
            if response.status_code == 200:
                data = response.json()
                for asset in data['assets']:  # 遍历下载链接
                    if isinstance(asset, dict) and 'browser_download_url' in asset:
                        asset_url.append(asset['browser_download_url'])
                self.phase = "down"
                self.phaseChange.emit(self.phase)
                return asset_url
            elif response.status_code == 403:  # 触发API限制
                logger.warning("到达Github API限制，请稍后再试")
                response = requests.get('https://api.github.com/users/octocat')
                reset_time = response.headers.get('X-RateLimit-Reset')
                reset_time = int(reset_time)
                logger.debug("重置：%s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reset_time)))
                self.phase = "down"
                self.phaseChange.emit(self.phase)
            else:
                logger.error(f"网络连接错误：{response.status_code}")
                self.phase = "down"
                self.phaseChange.emit(self.phase)
        except Exception as e:
            logger.error(f"获取下载链接错误: {e}")
            self.phase = "down"
            self.phaseChange.emit(self.phase)

class Version(QThread):
    valueChange = Signal(int)
    versionChange = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.is_paused = bool(0)  # 标记线程是否暂停
        self.progress_value = int(0)  # 进度值
        self.mutex = QMutex()  # 互斥锁，用于线程同步
        self.cond = QWaitCondition()  # 等待条件，用于线程暂停和恢复
        self.version = str("0")
        self.local = 0
        self.channel = "rel"
        self.force = False

    def pause_thread(self):
        with QMutexLocker(self.mutex):
            self.is_paused = True  # 设置线程为暂停状态

    def resume_thread(self):
        if self.is_paused:
            with QMutexLocker(self.mutex):
                self.is_paused = False  # 设置线程为非暂停状态
                self.cond.wakeOne()  # 唤醒一个等待的线程

    def run(self):
        with QMutexLocker(self.mutex):
            while self.is_paused:
                self.cond.wait(self.mutex)  # 当线程暂停时，等待条件满足
            if self.progress_value >= 100:
                self.progress_value = 0
                return  # 当进度值达到 100 时，重置为 0 并退出线程
            if self.force:
                self.version = self.getLatest(self.channel)
                self.versionChange.emit(self.version)
            else:
                if self.channel == "rel" and self.compareVersion(self.local,"rel"):
                    self.version = self.getLatest("rel")
                    self.versionChange.emit(self.version)
                    self.progress_value = 100
                elif self.channel == "dev"and (self.compareVersion(self.local,"rel") or self.compareVersion(self.local,"dev")):
                    if self.compareVersion(self.local,"rel"):
                        self.version = self.getLatest("rel")
                        self.versionChange.emit(self.version)
                        self.progress_value = 100
                    elif self.compareVersion(self.local,"dev"):
                        self.version = self.getLatest("dev")
                        self.versionChange.emit(self.version)
                        self.progress_value = 100
                else:
                    self.version = "latest"
                    self.versionChange.emit(self.version)
                    self.progress_value = 100

    def compareVersion(self,local:int,channel:str) -> bool | None:
        try:
            url = "https://raw.githubusercontent.com/NamePickerOrg/NamePicker/refs/heads/master/version.json"
            resp = requests.get(url,verify=False)
            if resp.status_code == 200:
                data = resp.json()
                return local < data["VERNO_%s"%channel]
            elif resp.status_code == 403:  # 触发API限制
                logger.warning("到达Github API限制，请稍后再试")
                resp = requests.get('https://api.github.com/users/octocat')
                reset_time = resp.headers.get('X-RateLimit-Reset')
                reset_time = datetime.fromtimestamp(int(reset_time))
                return False
            else:
                logger.error(f"网络连接错误：{resp.status_code}")
                return False
        except Exception as e:
            logger.error(f"错误: {e}")
            return False

    def getLatest(self,channel:str) -> str | None:
        try:
            url = "https://raw.githubusercontent.com/NamePickerOrg/NamePicker/refs/heads/master/version.json"
            resp = requests.get(url,verify=False)
            if resp.status_code == 200:
                data = resp.json()
                return data["version_%s"%channel]
            elif resp.status_code == 403:  # 触发API限制
                logger.warning("到达Github API限制，请稍后再试")
                resp = requests.get('https://api.github.com/users/octocat')
                reset_time = resp.headers.get('X-RateLimit-Reset')
                reset_time = datetime.fromtimestamp(int(reset_time))
            else:
                logger.error(f"网络连接错误：{resp.status_code}")
        except Exception as e:
            logger.error(f"错误: {e}")

if __name__ == "__main__":
    # dl = getDownloadUrl("NamePickerOrg","NamePicker","latest")
    # print(dl)
    # downloadAndExtract(getDownloadUrl("NamePickerOrg","NamePicker","latest")[1],"proto.zip")
    pass