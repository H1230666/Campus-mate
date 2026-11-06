Page({
  data: {
    errorTitle: '接口请求异常',
    errorDesc: '服务器开小差了，请稍后重试'
  },
  onLoad(options) {
    if(options.title) {
      this.setData({errorTitle: options.title})
    }
    if(options.desc) {
      this.setData({errorDesc: options.desc})
    }
  },
  onRetry() {
    wx.navigateBack()
  },
  backHome() {
    wx.switchTab({url:'/pages/index/index'})
  }
})
