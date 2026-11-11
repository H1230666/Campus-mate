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

function pad(value) {
  return value < 10 ? `0${value}` : `${value}`
}

function formatDateTime(value) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`
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
            statusLabel: STATUS_LABELS[detail.status] || detail.status,
            startTimeText: formatDateTime(detail.start_time)
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
