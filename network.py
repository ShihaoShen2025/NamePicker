import requests
from loguru import logger
import datetime

def getDownloadUrl(user,repo,reltag):
    try:
        url = f"https://api.github.com/repos/{user}/{repo}/releases/{reltag}"
        response = requests.get(url)
        asset_url = []
        if response.status_code == 200:
            data = response.json()
            for asset in data['assets']:  # 遍历下载链接
                if isinstance(asset, dict) and 'browser_download_url' in asset:
                    asset_url.append(asset['browser_download_url'])
            return asset_url
        elif response.status_code == 403:  # 触发API限制
            logger.warning("到达Github API限制，请稍后再试")
            response = requests.get('https://api.github.com/users/octocat')
            reset_time = response.headers.get('X-RateLimit-Reset')
            reset_time = datetime.fromtimestamp(int(reset_time))
        else:
            logger.error(f"网络连接错误：{response.status_code}")
    except Exception as e:
        logger.error(f"获取下载链接错误: {e}")

if __name__ == "__main__":
    dl = getDownloadUrl("NamePickerOrg","NamePicker","latest")
    print(dl)