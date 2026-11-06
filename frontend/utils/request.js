const baseUrl = "http://localhost:8000/api"


function request(options) {
  const token = wx.getStorageSync('token')
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'content-type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const data = res.data
          if (data.code === 200) {
            resolve(data)
          } else {
            wx.showToast({
              title: data.msg || '业务请求异常',
              icon: 'none',
              duration: 2000
            })
            reject(data)
          }
        } else {
          wx.showToast({
            title: `服务异常：${res.statusCode}`,
            icon: 'none'
          })
          reject(res)
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络连接失败，请检查网络',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

export default request
