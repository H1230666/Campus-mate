// 注册 / 完善资料：首次微信登录后补充昵称与兴趣标签
const API_BASE = "http://127.0.0.1:8000"

function toast(title) {
  wx.showToast({ title, icon: "none" })
}

Page({
  data: {
    nickname: "",
    tags: ""
  },

  onNicknameInput(e) {
    this.setData({ nickname: e.detail.value })
  },

  onTagsInput(e) {
    this.setData({ tags: e.detail.value })
  },

  submit() {
    const token = wx.getStorageSync("token")
    if (!token) {
      wx.redirectTo({ url: "/pages/login/login" })
      return
    }

    const nickname = this.data.nickname.trim()
    if (nickname.length < 1 || nickname.length > 32) {
      toast("昵称需要 1-32 个字符")
      return
    }

    const tags = this.data.tags
      .split(/[,，]/)
      .map(s => s.trim())
      .filter(Boolean)
    if (tags.length > 5) {
      toast("兴趣标签最多 5 个")
      return
    }

    wx.request({
      url: API_BASE + "/api/user/info",
      method: "PUT",
      header: { Authorization: "Bearer " + token },
      data: { nickname, interest_tags: tags },
      success: res => {
        const body = res.data || {}
        if (res.statusCode === 200 && body.code === 200) {
          wx.showToast({ title: "保存成功" })
          setTimeout(() => wx.navigateBack(), 600)
        } else {
          toast(body.msg || "保存失败")
        }
      },
      fail: () => toast("网络异常，请确认后端已启动")
    })
  }
})
