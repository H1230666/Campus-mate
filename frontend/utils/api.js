const app = getApp()

function request(path, data, options) {
  const opts = options || {}
  const method = opts.method || 'GET'
  const header = Object.assign({ 'content-type': 'application/json' }, opts.header || {})

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.apiBaseUrl}${path}`,
      data: data || {},
      method,
      header,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail(err) {
        reject(err)
      }
    })
  })
}

/**
 * 带临时登录身份的请求。
 * 登录接口（issue #2）合入前，用本地缓存 userId + X-User-Id 请求头模拟登录态；
 * 合入后改为携带 Authorization: Bearer <token> 即可，本文件是唯一改动点。
 *
 * 注意：没有 userId 时不再静默回退到 1，否则所有未登录用户都会写进同一个账号。
 */
function requestAsUser(path, data, options) {
  const userId = wx.getStorageSync('userId')
  if (!userId) {
    wx.showToast({ title: '请先登录后再操作', icon: 'none' })
    return Promise.reject({
      statusCode: 401,
      data: { code: 40101, message: '未登录，请先登录' }
    })
  }
  const opts = options || {}
  const header = Object.assign({ 'X-User-Id': String(userId) }, opts.header || {})
  return request(path, data, Object.assign({}, opts, { header }))
}

module.exports = { request, requestAsUser }
