const BASE_URL = process.env.VUE_APP_API_BASE_URL; // 后端API地址

// 调试信息
console.log(
  "🔗 环境变量 VUE_APP_API_BASE_URL:",
  process.env.VUE_APP_API_BASE_URL
);
console.log("🔗 实际使用的 BASE_URL:", BASE_URL);
console.log("🔗 当前环境 NODE_ENV:", process.env.NODE_ENV);

// 检查环境变量是否正确配置
if (!BASE_URL) {
  console.error("❌ 错误: VUE_APP_API_BASE_URL 环境变量未配置!");
  throw new Error("API基础地址未配置，请检查环境变量 VUE_APP_API_BASE_URL");
}

// 封装fetch请求
function request(url, options = {}) {
  const token = storage.getToken();
  if (token) {
    options.header = {
      ...options.header,
      Authorization: `Bearer ${token}`,
    };
  }
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      ...options,
      success: (res) => {
        // 检查响应状态
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          // 根据不同状态码提供更准确的错误信息
          let errorMsg = `HTTP ${res.statusCode}`;
          if (res.data && res.data.detail) {
            errorMsg += `: ${res.data.detail}`;
          }
          const error = new Error(errorMsg);
          error.statusCode = res.statusCode;
          error.responseData = res.data;
          reject(error);
        }
      },
      fail: (err) => {
        console.error("网络请求失败:", err);
        const error = new Error("网络请求失败，请检查网络连接");
        error.isNetworkError = true;
        reject(error);
      },
    });
  });
}

// 上传文件
function uploadFile(url, filePath, token) {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: BASE_URL + url,
      filePath: filePath,
      name: "file",
      header: {
        Authorization: `Bearer ${token}`,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const data = JSON.parse(res.data);
            resolve(data);
          } catch (e) {
            resolve(res.data);
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      },
      fail: (err) => {
        console.error("文件上传失败:", err);
        reject(new Error("文件上传失败"));
      },
    });
  });
}

// API接口
export const api = {
  // 用户注册
  register: (userData) => {
    return request("/auth/register", {
      method: "POST",
      data: userData,
      header: {
        "Content-Type": "application/json",
      },
    });
  },

  // 用户登录
  login: (loginData) => {
    return request("/auth/login", {
      method: "POST",
      data: loginData,
      header: {
        "Content-Type": "application/json",
      },
    });
  },

  // 更新用户邮箱
  updateUserEmail: (token, emailData) => {
    return request("/auth/users/me/email", {
      method: "PUT",
      data: emailData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 更新用户密码
  updateUserPassword: (token, passwordData) => {
    return request("/auth/users/me/password", {
      method: "PUT",
      data: passwordData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },
  // 获取用户信息
  getUserInfo: (token) => {
    return request("/auth/users/me", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 更新用户信息
  updateUserInfo: (token, userData) => {
    return request("/auth/users/me", {
      method: "PUT",
      data: userData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取用户日记
  getUserDiaries: (token) => {
    return request("/diary/", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取单个日记详情
  getDiary: (diaryId, token) => {
    return request(`/diary/${diaryId}`, {
      method: "GET",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 创建日记
  createDiary: (token, diaryData) => {
    return request("/diary/", {
      method: "POST",
      data: diaryData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 删除日记
  deleteDiary: (token, diaryId) => {
    return request(`/diary/${diaryId}`, {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取心情统计数据
  getMoodStats: (token, period) => {
    return request(`/diary/mood-stats/${period}`, {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  // 获取成长指数
  getGrowthScore: (token) => {
    return request("/diary/growth-score", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  // 上传图片
  uploadImage: (filePath, token) => {
    return uploadFile("/image/upload", filePath, token);
  },

  // 上传日记背景图片
  uploadDiaryBackground: (filePath, token) => {
    return uploadFile("/diary-backgrounds/upload", filePath, token);
  },

  // 获取用户的背景图片列表
  getUserBackgrounds: (token) => {
    return request("/diary-backgrounds/list", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 删除背景图片
  deleteDiaryBackground: (token, backgroundId) => {
    return request(`/diary-backgrounds/${backgroundId}`, {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取默认背景选项
  getDefaultBackgrounds: () => {
    return request("/diary-backgrounds/default");
  },

  // 恢复默认背景
  restoreDefaultBackgrounds: (token) => {
    return request("/diary-backgrounds/restore-default", {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 创建反馈
  createFeedback: (token, feedbackData) => {
    return request("/feedback/", {
      method: "POST",
      data: feedbackData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },
  // 创建悄悄话
  createWhisper: (token, whisperData) => {
    return request("/tree-hole/", {
      method: "POST",
      data: whisperData,
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取用户悄悄话
  getUserWhispers: (token) => {
    return request("/tree-hole/my-whispers", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  getRandomWhisper: (token) => {
    return request("/tree-hole/random", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  likeWhisper: (token, whisperId) => {
    return request(`/tree-hole/${whisperId}/like`, {
      method: "POST",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  getWhisperDetails: (token, whisperId) => {
    return request(`/tree-hole/${whisperId}`, {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  getWhisperChatHistory: (token, whisperId) => {
    return request(`/tree-hole-chat/${whisperId}`, {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  sendWhisperChatMessage: (token, whisperId, content) => {
    return request(`/tree-hole-chat/${whisperId}`, {
      method: "POST",
      data: { content },
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  },
  getMyPostedWhispers: (token) => {
    return request("/tree-hole/my-whispers", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  getMyChats: (token) => {
    return request("/tree-hole-chat/chats/", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
  // 删除悄悄话
  deleteWhisper: (token, whisperId) => {
    return request(`/tree-hole/${whisperId}`, {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 退出聊天
  leaveWhisperChat: (token, whisperId) => {
    return request(`/tree-hole-chat/${whisperId}/leave`, {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取风险评估报告历史
  getRiskAssessmentReports: (token, limit = 10) => {
    return request(`/risk-assessment/reports-history?limit=${limit}`, {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 获取风险评估统计信息
  getRiskAssessmentStats: (token) => {
    return request("/risk-assessment/statistics", {
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // 用户日记背景管理
  getUserDiaryBackgrounds: (token) => {
    return request("/user-diary-backgrounds", {
      method: "GET",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  uploadUserDiaryBackground: (filePath, token) => {
    return uploadFile("/user-diary-backgrounds/upload", filePath, token);
  },

  deleteUserDiaryBackground: (token, backgroundId) => {
    return request(`/user-diary-backgrounds/${backgroundId}`, {
      method: "DELETE",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  restoreDefaultDiaryBackgrounds: (token) => {
    return request("/user-diary-backgrounds/restore-default", {
      method: "POST",
      header: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

// 本地存储工具
export const storage = {
  setToken: (token) => {
    uni.setStorageSync("access_token", token);
  },

  getToken: () => {
    return uni.getStorageSync("access_token");
  },

  clearToken: () => {
    uni.removeStorageSync("access_token");
  },

  setUserInfo: (userInfo) => {
    uni.setStorageSync("user_info", JSON.stringify(userInfo));
  },

  getUserInfo: () => {
    const userInfo = uni.getStorageSync("user_info");
    return userInfo ? JSON.parse(userInfo) : null;
  },

  clearUserInfo: () => {
    uni.removeStorageSync("user_info");
  },
};
