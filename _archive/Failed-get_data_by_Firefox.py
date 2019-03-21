base_url = "http://www.cninfo.com.cn/cninfo-new/index#"
profile = webdriver.FirefoxProfile(r'G:\Program\Projects\Apolo\firefox_profile')
profile.set_preference('browser.download.dir', 'G:\Program\Projects\Apolo\data')  # to set the path for download
profile.set_preference('browser.download.folderList', 2)  # customize download path, 1 is download to default path, 0 is default path
profile.set_preference('browser.download.manager.showWhenStarting', True)  # display the download dialog or not
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')  # the type of download.
driver = webdriver.Firefox(firefox_profile=profile)
# driver = webdriver.Firefox(profile)