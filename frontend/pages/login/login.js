// 后端地址集中配置：真机调试时改成电脑的局域网 IP
const API_BASE = "http://127.0.0.1:8000"
// 个人主页（v0.2.0 上线，未创建时跳转失败有兜底提示）
const PROFILE_PAGE = "/pages/profile/index"

function toast(title) {
  wx.showToast({ title, icon: "none" })
}

Page({
  data: {
    account: "",
    pwd: "",
    isAgree: false,
    loading: false
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
    if (this.data.loading) return
    if (!this.data.isAgree) {
      toast("请先勾选用户协议")
      return
    }
    if (!this.data.account || !this.data.pwd) {
      toast("请输入账号和密码")
      return
    }
    this.post("/account-login", {
      account: this.data.account,
      password: this.data.pwd
    })
  },

  // 微信一键登录
  handleLogin() {
    if (this.data.loading) return
    if (!this.data.isAgree) {
      toast("请先勾选用户协议")
      return
    }
    wx.login({
      success: res => {
        if (!res.code) {
          toast("获取微信授权码失败，请重试")
          return
        }
        this.post("/api/user/wx-login", { code: res.code })
      },
      // 用户拒绝授权、微信客户端异常都会走到这里，不能只靠 success
      fail: () => {
        toast("已取消微信授权，可改用账号密码登录")
      }
    })
  },

  // 统一请求处理：判断 HTTP 状态与业务 code，避免后端返回 401 也提示“登录成功”
  post(path, data) {
    this.setData({ loading: true })
    wx.request({
      url: API_BASE + path,
      method: "POST",
      data,
      success: res => {
        const body = res.data || {}
        if (res.statusCode === 200 && body.code === 200) {
          this.onLoginSuccess(body.data || {})
        } else {
          toast(body.msg || "登录失败，请检查账号或密码")
        }
      },
      fail: () => {
        toast("网络异常，请确认后端服务已启动")
      },
      complete: () => {
        this.setData({ loading: false })
      }
    })
  },

  // 登录成功：存 token 并跳转个人主页
  onLoginSuccess(data) {
    if (data.token) {
      wx.setStorageSync("token", data.token)
    }
    wx.showToast({ title: "登录成功" })
    wx.navigateTo({
      url: PROFILE_PAGE,
      fail: () => {
        // 个人主页尚未创建时不阻塞登录流程
        toast("登录成功，个人主页将在 v0.2.0 上线")
      }
    })
  }
})
