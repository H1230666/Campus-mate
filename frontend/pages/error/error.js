// frontend/pages/error/error.js
Page({
  data: {},
  onRetry() {
    wx.navigateBack({delta:1})
  },
  goHome() {
    wx.switchTab({url:"/pages/index/index"})
  }
})
