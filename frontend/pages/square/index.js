const api = require('../../utils/api')

const TYPES = [
  { key: '', label: '全部' },
  { key: 'study', label: '学习' },
  { key: 'sport', label: '运动' },
  { key: 'food', label: '美食' },
  { key: 'travel', label: '出行' },
  { key: 'other', label: '其他' }
]

const TYPE_LABELS = {
  study: '学习',
  sport: '运动',
  food: '美食',
  travel: '出行',
  other: '其他'
}

Page({
  data: {
    types: TYPES,
    activeType: '',
    invitations: [],
    page: 1,
    pageSize: 10,
    total: 0,
    loading: false,
    hasMore: true,
    error: false,
    empty: false
  },

  onLoad() {
    this.fetchList(true)
  },

  onPullDownRefresh() {
    this.fetchList(true).finally(() => wx.stopPullDownRefresh())
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.fetchList(false)
    }
  },

  onFilterTap(e) {
    const key = e.currentTarget.dataset.key
    if (key === this.data.activeType) return
    this.setData({ activeType: key })
    this.fetchList(true)
  },

  onRetry() {
    this.fetchList(true)
  },

  fetchList(reset) {
    if (this.data.loading) return Promise.resolve()
    const page = reset ? 1 : this.data.page + 1
    const params = { page, page_size: this.data.pageSize }
    if (this.data.activeType) {
      params.type = this.data.activeType
    }
    this.setData({ loading: true, error: false })
    return api
      .request('/api/invitations', params)
      .then((data) => {
        const items = data.list.map((item) => ({
          ...item,
          typeLabel: TYPE_LABELS[item.type] || item.type
        }))
        const list = reset ? items : this.data.invitations.concat(items)
        this.setData({
          invitations: list,
          page,
          total: data.total,
          hasMore: page * this.data.pageSize < data.total,
          empty: list.length === 0
        })
      })
      .catch(() => {
        this.setData({ error: true })
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  goDetail(e) {
    wx.navigateTo({
      url: `/pages/invitation/index?id=${e.currentTarget.dataset.id}`
    })
  }
})
