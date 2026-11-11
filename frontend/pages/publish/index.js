const api = require('../../utils/api')

const DRAFT_KEY = 'publish_draft'
const MAX_DESCRIPTION = 500
const MIN_MAX_COUNT = 2
const MAX_MAX_COUNT = 20
const MIN_LEAD_MINUTES = 10

const TYPES = [
  { key: 'study', label: '学习' },
  { key: 'sport', label: '运动' },
  { key: 'food', label: '美食' },
  { key: 'travel', label: '出行' },
  { key: 'other', label: '其他' }
]

function pad(value) {
  return value < 10 ? `0${value}` : `${value}`
}

function formatDate(date) {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
}

function addDays(date, days) {
  const next = new Date(date)
  next.setDate(next.getDate() + days)
  return next
}

function splitDateTime(value) {
  if (!value) {
    return { date: '', time: '' }
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return { date: '', time: '' }
  }
  return {
    date: formatDate(date),
    time: `${pad(date.getHours())}:${pad(date.getMinutes())}`
  }
}

Page({
  data: {
    types: TYPES,
    typeIndex: -1,
    typeLabel: '',
    form: {
      title: '',
      type: '',
      location: '',
      date: '',
      time: '19:00',
      maxCount: 4,
      description: ''
    },
    errors: {},
    canSubmit: false,
    submitting: false,
    today: '',
    maxDate: '',
    descriptionLength: 0,
    draftTip: ''
  },

  onLoad() {
    const now = new Date()
    this.setData({
      today: formatDate(now),
      maxDate: formatDate(addDays(now, 30))
    })
    this.restoreDraft()
  },

  onUnload() {
    this.persistLocalDraft()
  },

  restoreDraft() {
    const local = wx.getStorageSync(DRAFT_KEY)
    if (local && local.form) {
      this.applyForm(local.form, '已恢复上次未提交的本地草稿')
      return
    }
    this.loadServerDraft()
  },

  loadServerDraft() {
    api
      .requestAsUser('/api/invitations/draft')
      .then((draft) => {
        if (!draft) return
        const time = splitDateTime(draft.start_time)
        this.applyForm(
          {
            title: draft.title || '',
            type: draft.type || '',
            location: draft.location || '',
            date: time.date,
            time: time.time || '19:00',
            maxCount: draft.max_count || 4,
            description: draft.description || ''
          },
          '已恢复服务端草稿'
        )
      })
      .catch(() => {})
  },

  applyForm(form, tip) {
    const typeIndex = TYPES.findIndex((item) => item.key === form.type)
    const merged = Object.assign({}, this.data.form, form)
    this.setData(
      {
        form: merged,
        typeIndex,
        typeLabel: typeIndex >= 0 ? TYPES[typeIndex].label : '',
        descriptionLength: (merged.description || '').length,
        draftTip: tip || ''
      },
      () => this.refreshCanSubmit()
    )
  },

  updateField(field, value) {
    const patch = {}
    patch[`form.${field}`] = value
    patch[`errors.${field}`] = ''
    this.setData(patch, () => {
      this.refreshCanSubmit()
      this.scheduleLocalSave()
    })
  },

  onTitleInput(event) {
    this.updateField('title', event.detail.value)
  },

  onLocationInput(event) {
    this.updateField('location', event.detail.value)
  },

  onDescriptionInput(event) {
    const value = event.detail.value
    this.setData(
      {
        'form.description': value,
        'errors.description': '',
        descriptionLength: value.length
      },
      () => {
        this.refreshCanSubmit()
        this.scheduleLocalSave()
      }
    )
  },

  onTypeChange(event) {
    const index = Number(event.detail.value)
    const type = TYPES[index]
    if (!type) return
    this.setData(
      {
        typeIndex: index,
        typeLabel: type.label,
        'form.type': type.key,
        'errors.type': ''
      },
      () => {
        this.refreshCanSubmit()
        this.scheduleLocalSave()
      }
    )
  },

  onDateChange(event) {
    this.updateField('date', event.detail.value)
  },

  onTimeChange(event) {
    this.updateField('time', event.detail.value)
  },

  changeCount(event) {
    const delta = Number(event.currentTarget.dataset.delta)
    const next = Math.min(MAX_MAX_COUNT, Math.max(MIN_MAX_COUNT, this.data.form.maxCount + delta))
    if (next === this.data.form.maxCount) return
    this.updateField('maxCount', next)
  },

  refreshCanSubmit() {
    const form = this.data.form
    const canSubmit = Boolean(
      form.title.trim() &&
        form.type &&
        form.location.trim() &&
        form.date &&
        form.time &&
        !this.data.submitting
    )
    this.setData({ canSubmit })
  },

  composeStartTime() {
    const { date, time } = this.data.form
    if (!date || !time) return null
    // 选择器给的是手机本地时间；toISOString() 统一转成 UTC，后端按 UTC 存储与校验
    const start = new Date(`${date}T${time}:00`)
    return Number.isNaN(start.getTime()) ? null : start
  },

  validate() {
    const form = this.data.form
    const errors = {}
    const title = form.title.trim()
    const location = form.location.trim()

    if (title.length < 4 || title.length > 30) {
      errors.title = '标题需 4-30 个字符'
    }
    if (!form.type) {
      errors.type = '请选择搭子类型'
    }
    if (location.length < 2 || location.length > 50) {
      errors.location = '地点需 2-50 个字符'
    }
    if (!form.date) {
      errors.date = '请选择日期'
    }
    if (!form.time) {
      errors.time = '请选择时间'
    }

    const start = this.composeStartTime()
    if (start && start.getTime() < Date.now() + MIN_LEAD_MINUTES * 60 * 1000) {
      errors.time = `开始时间需晚于当前 ${MIN_LEAD_MINUTES} 分钟`
    }
    if (form.maxCount < MIN_MAX_COUNT || form.maxCount > MAX_MAX_COUNT) {
      errors.maxCount = `人数需在 ${MIN_MAX_COUNT}-${MAX_MAX_COUNT} 之间`
    }
    if (form.description.length > MAX_DESCRIPTION) {
      errors.description = `备注最多 ${MAX_DESCRIPTION} 字`
    }

    this.setData({ errors })
    return Object.keys(errors).length === 0
  },

  onSubmit() {
    if (this.data.submitting) return
    if (!this.validate()) {
      const firstError = Object.values(this.data.errors)[0]
      wx.showToast({ title: firstError || '请检查表单填写', icon: 'none' })
      return
    }

    const form = this.data.form
    const start = this.composeStartTime()
    if (!start) {
      wx.showToast({ title: '请选择有效的开始时间', icon: 'none' })
      return
    }
    this.setData({ submitting: true, draftTip: '' }, () => this.refreshCanSubmit())

    api
      .requestAsUser(
        '/api/invitations',
        {
          title: form.title.trim(),
          type: form.type,
          location: form.location.trim(),
          start_time: start.toISOString(),
          max_count: form.maxCount,
          description: form.description.trim() || null
        },
        { method: 'POST' }
      )
      .then(() => {
        wx.removeStorageSync(DRAFT_KEY)
        wx.showToast({ title: '发布成功', icon: 'success' })
        setTimeout(() => {
          wx.navigateBack({
            fail: () => wx.redirectTo({ url: '/pages/square/index' })
          })
        }, 800)
      })
      .catch((res) => this.handleSubmitError(res))
      .finally(() => {
        this.setData({ submitting: false }, () => this.refreshCanSubmit())
      })
  },

  handleSubmitError(res) {
    if (res && res.statusCode === 401) {
      wx.showToast({ title: '请先登录后再发布', icon: 'none' })
      return
    }
    if (res && res.statusCode === 422 && res.data && Array.isArray(res.data.detail)) {
      const errors = {}
      res.data.detail.forEach((item) => {
        const last = item.loc && item.loc[item.loc.length - 1]
        const field = last === 'start_time' ? 'time' : last
        if (field) {
          errors[field] = String(item.msg).replace('Value error, ', '')
        }
      })
      this.setData({ errors })
      wx.showToast({ title: '请检查表单填写', icon: 'none' })
      return
    }
    wx.showToast({ title: '发布失败，请稍后重试', icon: 'none' })
  },

  onSaveDraft() {
    if (this.data.submitting) return
    this.persistLocalDraft()

    const form = this.data.form
    const start = this.composeStartTime()
    this.setData({ draftTip: '正在保存…' })

    api
      .requestAsUser(
        '/api/invitations/draft',
        {
          title: form.title.trim(),
          type: form.type || null,
          location: form.location.trim(),
          start_time: start ? start.toISOString() : null,
          max_count: form.maxCount,
          description: form.description.trim() || null
        },
        { method: 'PUT' }
      )
      .then(() => this.setData({ draftTip: '草稿已保存，下次进入会自动恢复' }))
      .catch((res) => {
        const tip =
          res && res.statusCode === 401
            ? '请先登录后再保存到服务端'
            : '已保存到本地，服务端暂不可用'
        this.setData({ draftTip: tip })
      })
  },

  scheduleLocalSave() {
    clearTimeout(this.saveTimer)
    this.saveTimer = setTimeout(() => this.persistLocalDraft(), 600)
  },

  persistLocalDraft() {
    const form = this.data.form
    if (!form.title && !form.location && !form.description) return
    wx.setStorageSync(DRAFT_KEY, { form, savedAt: Date.now() })
  }
})
