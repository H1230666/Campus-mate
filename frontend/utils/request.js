// frontend/utils/request.js
const baseUrl = "http://127.0.0.1:8000"; // 后端接口地址，上线改成真实地址
const showToast = (msg) => {
  wx.showToast({
    title: msg,
    icon: "none",
    duration: 2000
  })
}

const request = (options) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl + options.url,
      method: options.method || "GET",
      data: options.data || {},
      header: {
        "content-type": "application/json",
        "Authorization": wx.getStorageSync("token") || ""
      },
      success: (res) => {
        // 捕获后端错误码
        if (res.statusCode >= 200 && res.statusCode < 300) {
          if (res.data.code !== 0) {
            showToast(res.data.msg || "业务请求异常");
            reject(res.data);
            return;
          }
          resolve(res.data);
        } else if (res.statusCode === 401) {
          showToast("登录已失效，请重新登录");
          wx.navigateTo({url: "/pages/login/login"});
          reject(res);
        } else if (res.statusCode === 404) {
          wx.navigateTo({url: "/pages/error/error"});
          reject(res);
        } else {
          showToast(`服务器错误：${res.statusCode}`);
          reject(res);
        }
      },
      fail: (err) => {
        // 网络失败、断网
        showToast("网络请求失败，请检查网络");
        wx.navigateTo({url: "/pages/error/error"});
        reject(err);
      }
    })
  })
}

export default request;
