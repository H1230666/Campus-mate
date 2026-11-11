// 个人主页：校验登录态并展示用户信息
const API_BASE = "http://127.0.0.1:8000"

function toast(title) {
  wx.showToast({ title, icon: "none" })
}

Page({
  data: {
    openid: "",
    nickname: "",
    avatar: "",
    tags: [],
    loading: true
  },

  onShow() {
    this.loadProfile()
  },

  // 拉取个人信息；token 缺失或失效都退回登录页
  loadProfile() {
    const token = wx.getStorageSync("token")
    if (!token) {
      wx.redirectTo({ url: "/pages/login/login" })
      return
    }
    wx.request({
      url: API_BASE + "/api/user/info",
      method: "GET",
      header: { Authorization: "Bearer " + token },
      success: res => {
        if (res.statusCode === 401) {
          wx.removeStorageSync("token")
          wx.redirectTo({ url: "/pages/login/login" })
          return
        }
        const body = res.data || {}
        if (body.code === 200) {
          const d = body.data || {}
          this.setData({
            openid: d.openid || "",
            nickname: d.nickname || "校园搭子用户",
            avatar: d.avatar || "",
            tags: d.interest_tags || [],
            loading: false
          })
        } else {
          toast(body.msg || "加载失败")
          this.setData({ loading: false })
        }
      },
      fail: () => {
        toast("网络异常，请确认后端已启动")
        this.setData({ loading: false })
      }
    })
  },

  goEdit() {
    wx.navigateTo({ url: "/pages/register/index" })
  },

  logout() {
    wx.removeStorageSync("token")
    wx.reLaunch({ url: "/pages/login/login" })
  }
})
