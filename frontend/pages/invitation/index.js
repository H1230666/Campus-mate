const api = require('../../utils/api')

const TYPE_LABELS = {
  study: '学习',
  sport: '运动',
  food: '美食',
  travel: '出行',
  other: '其他'
}

const STATUS_LABELS = {
  recruiting: '招募中',
  full: '已满'
}

Page({
  data: {
    detail: null,
    loading: true,
    error: false,
    notFound: false
  },

  onLoad(options) {
    this.invitationId = options.id
    this.fetchDetail()
  },

  fetchDetail() {
    this.setData({ loading: true, error: false, notFound: false })
    api
      .request(`/api/invitations/${this.invitationId}`)
      .then((detail) => {
        this.setData({
          detail: {
            ...detail,
            typeLabel: TYPE_LABELS[detail.type] || detail.type,
            statusLabel: STATUS_LABELS[detail.status] || detail.status
          },
          loading: false
        })
      })
      .catch((res) => {
        const notFound = !!(res && res.statusCode === 404)
        this.setData({
          loading: false,
          notFound,
          error: !notFound
        })
      })
  },

  onRetry() {
    this.fetchDetail()
  },

  onBack() {
    wx.navigateBack()
  }
})
