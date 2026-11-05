Page({
  data: {
    account: "",
    pwd: "",
    isAgree: false
  },
  onAccountInput(e) {
    this.setData({ account: e.detail.value })
  },
  onPwdInput(e) {
    this.setData({ pwd: e.detail.value })
  },
  toggleAgree() {
    this.setData({ isAgree: !this.data.isAgree })
  },
  // 账号密码登录
  accountLogin() {
    if (!this.data.isAgree) {
      wx.showToast({ title: "请勾选协议", icon: "none" })
      return
    }
    wx.request({
      url: "http://127.0.0.1:8000/account-login",
      method: "POST",
      data: {
        account: this.data.account,
        password: this.data.pwd
      },
      success: res => {
        wx.showToast({ title: "登录成功" })
      },
      fail: () => {
        wx.showToast({ title: "后端未启动", icon: "none" })
      }
    })
  },
  // 微信一键登录
  handleLogin() {
    if (!this.data.isAgree) {
      wx.showToast({ title: "请勾选协议", icon: "none" })
      return
    }
    wx.login({
      success: res => {
        console.log("code：", res.code)
        wx.request({
          url: "http://127.0.0.1:8000/login",
          method: "POST",
          data: { code: res.code },
          success: (res) => {
            wx.showToast({ title: "微信登录成功" })
          },
          fail: () => {
            wx.showToast({ title: "后端未启动", icon: "none" })
          }
        })
      }
    })
  }
})
