// const BASE_URL = 'http://127.0.0.1:8000'; // 后端API地址

// // 封装fetch请求
// function request(url, options = {}) {
//     return new Promise((resolve, reject) => {
//         uni.request({
//             url: BASE_URL + url,
//             ...options,
//             success: (res) => {
//                 // 检查响应状态
//                 if (res.statusCode >= 200 && res.statusCode < 300) {
//                     resolve(res.data);
//                 } else {
//                     reject(new Error(`HTTP ${res.statusCode}: ${res.data?.detail || '请求失败'}`));
//                 }
//             },
//             fail: (err) => {
//                 console.error('请求失败:', err);
//                 reject(new Error('网络请求失败，请检查网络连接'));
//             }
//         });
//     });
// }

// // API接口
// export const api = {
//     // 用户注册
//     register: (userData) => {
//         return request('/auth/register', {
//             method: 'POST',
//             data: userData,
//             header: {
//                 'Content-Type': 'application/json'
//             }
//         });
//     },
    
//     // 用户登录
//     login: (loginData) => {
//         return request('/auth/login', {
//             method: 'POST',
//             data: loginData,
//             header: {
//                 'Content-Type': 'application/json'
//             }
//         });
//     },
    
//     // 获取用户信息
//     getUserInfo: (token) => {
//         return request('/auth/users/me', {
//             header: {
//                 'Authorization': `Bearer ${token}`
//             }
//         });
//     }
// };

// // 本地存储工具
// export const storage = {
//     setToken: (token) => {
//         uni.setStorageSync('access_token', token);
//     },
    
//     getToken: () => {
//         return uni.getStorageSync('access_token');
//     },
    
//     clearToken: () => {
//         uni.removeStorageSync('access_token');
//     },
    
//     setUserInfo: (userInfo) => {
//         uni.setStorageSync('user_info', JSON.stringify(userInfo));
//     },
    
//     getUserInfo: () => {
//         const userInfo = uni.getStorageSync('user_info');
//         return userInfo ? JSON.parse(userInfo) : null;
//     }
// };
const BASE_URL = 'http://127.0.0.1:8000'; // 后端API地址

// 封装fetch请求
function request(url, options = {}) {
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
                console.error('网络请求失败:', err);
                const error = new Error('网络请求失败，请检查网络连接');
                error.isNetworkError = true;
                reject(error);
            }
        });
    });
}

// API接口
export const api = {
    // 用户注册
    register: (userData) => {
        return request('/auth/register', {
            method: 'POST',
            data: userData,
            header: {
                'Content-Type': 'application/json'
            }
        });
    },

    // 用户登录
    login: (loginData) => {
        return request('/auth/login', {
            method: 'POST',
            data: loginData,
            header: {
                'Content-Type': 'application/json'
            }
        });
    },

    // 获取用户信息
    getUserInfo: (token) => {
        return request('/auth/users/me', {
            header: {
                'Authorization': `Bearer ${token}`
            }
        });
    }
};

// 本地存储工具
export const storage = {
    setToken: (token) => {
        uni.setStorageSync('access_token', token);
    },

    getToken: () => {
        return uni.getStorageSync('access_token');
    },

    clearToken: () => {
        uni.removeStorageSync('access_token');
    },

    setUserInfo: (userInfo) => {
        uni.setStorageSync('user_info', JSON.stringify(userInfo));
    },

    getUserInfo: () => {
        const userInfo = uni.getStorageSync('user_info');
        return userInfo ? JSON.parse(userInfo) : null;
    }
};