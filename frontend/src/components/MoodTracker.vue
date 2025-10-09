<template>
    <view class="mood-tracker-container">
        <text class="overview-title">心情晴雨表</text>

        <!-- 7天心情表格 -->
        <view class="weekly-mood">
            <text class="section-subtitle">最近7天心情记录</text>
            <view class="mood-table-container">
                <!-- 第一行：日期 -->
                <view class="table-row dates-row">
                    <view class="table-cell header-cell">日期</view>
                    <view v-for="(date, index) in weeklyMoodData.dates" :key="'date-' + index"
                        class="table-cell date-cell">
                        {{ formatShortDate(date) }}
                    </view>
                </view>
                <!-- 第二行：心情评分 -->
                <view class="table-row levels-row">
                    <view class="table-cell header-cell">心情</view>
                    <view v-for="(level, index) in weeklyMoodData.levels" :key="'level-' + index"
                        class="table-cell level-cell" :class="{ 'has-data': level }">
                        {{ level ? getMoodIcon(level) : "--" }}
                    </view>
                </view>
            </view>
        </view>

        <!-- 心情打分按钮 -->
        <view class="mood-rating-section">
            <text class="rating-label">今天的心情如何？给自己打个分吧</text>

            <!-- 未登录提示 -->
            <view v-if="!isLoggedIn" class="login-prompt">
                <text class="prompt-text">请先登录以记录心情</text>
                <view class="login-btn" @click="handleGoToLogin">
                    <text class="login-text">去登录</text>
                </view>
            </view>

            <!-- 已登录时的心情选择 -->
            <template v-else>
                <view class="mood-buttons">
                    <view v-for="level in [1, 2, 3, 4, 5]" :key="level" class="mood-btn"
                        :class="{ active: selectedMood === level }" @click="selectMood(level)">
                        <text class="mood-icon">{{ getMoodIcon(level) }}</text>
                        <text class="mood-desc">{{ getMoodDesc(level) }}</text>
                    </view>
                </view>
                <view v-if="selectedMood" class="save-btn" @click="saveMood">
                    <text class="save-text">保存今日心情</text>
                </view>
            </template>
        </view>
    </view>
</template>

<script>
export default {
    name: 'MoodTracker',
    props: {
        isLoggedIn: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            selectedMood: null,
            weeklyMoodData: {
                dates: [],
                levels: [],
            }
        }
    },
    mounted() {
        this.loadWeeklyMood();
    },
    watch: {
        isLoggedIn(newVal) {
            if (newVal) {
                this.loadWeeklyMood();
            } else {
                this.weeklyMoodData = {
                    dates: [],
                    levels: [],
                };
            }
        }
    },
    methods: {
        // 格式化短日期显示
        formatShortDate(dateStr) {
            if (!dateStr) return "--";
            const date = new Date(dateStr);
            const month = date.getMonth() + 1;
            const day = date.getDate();
            return `${month}/${day}`;
        },

        // 获取心情等级描述
        getMoodDesc(level) {
            const descriptions = {
                1: "很不满意",
                2: "有点失落",
                3: "还过得去",
                4: "挺满意的",
                5: "超级棒",
            };
            return descriptions[level] || "";
        },

        // 获取心情等级图标
        getMoodIcon(level) {
            const icons = {
                1: "😤",
                2: "😕",
                3: "😐",
                4: "😊",
                5: "🤩",
            };
            return icons[level] || "";
        },

        selectMood(level) {
            this.selectedMood = level;
        },

        handleGoToLogin() {
            this.$emit('go-to-login');
        },

        async saveMood() {
            if (!this.selectedMood) {
                uni.showToast({
                    title: "请选择心情档位",
                    icon: "none",
                });
                return;
            }

            // 检查是否已登录
            const token = uni.getStorageSync("access_token");
            if (!token) {
                uni.showModal({
                    title: "提示",
                    content: "请先登录账户",
                    success: (res) => {
                        if (res.confirm) {
                            this.handleGoToLogin();
                        }
                    },
                });
                return;
            }

            try {
                uni.showLoading({ title: "保存中..." });

                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/mood-tracker/mood`,
                    method: "POST",
                    header: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    data: {
                        mood_level: this.selectedMood,
                    },
                });

                if (response.statusCode === 200) {
                    // 显示积分奖励信息
                    const starMessage = response.data.star_message || "心情记录成功 💫";
                    uni.showToast({
                        title: starMessage,
                        icon: "none",
                        duration: 2500
                    });

                    // 重新加载7天数据
                    await this.loadWeeklyMood();

                    // 清除选择
                    this.selectedMood = null;

                    // 通知父组件心情保存成功，包含星星奖励信息
                    this.$emit('mood-saved', {
                        level: this.selectedMood,
                        data: response.data,
                        star_awarded: response.data.star_awarded,
                        star_points: response.data.star_points,
                        star_message: response.data.star_message
                    });
                } else if (response.statusCode === 401) {
                    uni.showModal({
                        title: "登录已过期",
                        content: "请重新登录",
                        success: (res) => {
                            if (res.confirm) {
                                uni.removeStorageSync("access_token");
                                this.handleGoToLogin();
                            }
                        },
                    });
                } else {
                    throw new Error(response.data?.detail || "保存失败");
                }
            } catch (error) {
                console.error("保存心情失败:", error);
                uni.showToast({
                    title: error.message || "保存失败",
                    icon: "none",
                });
            } finally {
                uni.hideLoading();
            }
        },

        async loadWeeklyMood() {
            const token = uni.getStorageSync("access_token");

            // 如果没有token，显示空数据
            if (!token) {
                this.weeklyMoodData = {
                    dates: [],
                    levels: [],
                };
                return;
            }

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL}/mood-tracker/mood/weekly`,
                    method: "GET",
                    header: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.statusCode === 200) {
                    this.weeklyMoodData = response.data;

                    // 通知父组件数据加载完成
                    this.$emit('data-loaded', response.data);
                } else if (response.statusCode === 401) {
                    // Token过期，清除本地存储
                    uni.removeStorageSync("access_token");
                    this.weeklyMoodData = {
                        dates: [],
                        levels: [],
                    };
                    this.$emit('login-expired');
                }
            } catch (error) {
                console.error("加载心情数据失败:", error);
                // 出错时显示空数据
                this.weeklyMoodData = {
                    dates: [],
                    levels: [],
                };
                this.$emit('load-error', error);
            }
        },

        // 提供给父组件调用的方法
        refreshData() {
            this.loadWeeklyMood();
        }
    }
}
</script>

<style scoped>
.mood-tracker-container {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10rpx);
    border-radius: 20rpx;
    padding: 32rpx;
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
    border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.overview-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    display: block;
}

/* 心情晴雨表样式 */
.mood-rating-section {
    padding: 32rpx 24rpx;
    background: rgba(248, 250, 252, 0.8);
    border-radius: 20rpx;
    border: 1rpx solid rgba(226, 232, 240, 0.8);
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.rating-label {
    font-size: 28rpx;
    color: #1e293b;
    margin-bottom: 32rpx;
    display: block;
    text-align: center;
    font-weight: 600;
    letter-spacing: 0.5rpx;
}

.mood-buttons {
    display: flex;
    justify-content: space-between;
    gap: 12rpx;
    margin-bottom: 32rpx;
}

.mood-btn {
    flex: 1;
    height: 120rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    border: 2rpx solid #e2e8f0;
    border-radius: 16rpx;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    gap: 8rpx;
    position: relative;
    overflow: hidden;
}

.mood-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent);
    transition: left 0.5s;
}

.mood-btn:hover::before {
    left: 100%;
}

.mood-btn.active {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-color: #1d4ed8;
    transform: translateY(-2rpx);
    box-shadow: 0 8rpx 25rpx rgba(59, 130, 246, 0.25);
}

.mood-icon {
    font-size: 36rpx;
    line-height: 1;
}

.mood-desc {
    font-size: 22rpx;
    font-weight: 500;
    color: #64748b;
    letter-spacing: 0.3rpx;
}

.mood-btn.active .mood-desc {
    color: #ffffff;
    font-weight: 600;
}

.save-btn {
    background: linear-gradient(135deg, #7dd3fc, #0ea5e9);
    color: white;
    padding: 28rpx 32rpx;
    border-radius: 16rpx;
    text-align: center;
    box-shadow: 0 4rpx 14rpx rgba(14, 165, 233, 0.25);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
    position: relative;
    overflow: hidden;
}

.save-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent);
    transition: left 0.6s;
}

.save-btn:active::before {
    left: 100%;
}

.save-btn:active {
    transform: translateY(1rpx);
    box-shadow: 0 2rpx 8rpx rgba(14, 165, 233, 0.4);
}

.save-text {
    font-size: 28rpx;
    font-weight: 600;
    letter-spacing: 0.5rpx;
}

.weekly-mood {
    margin-bottom: 32rpx;
    padding: 24rpx;
    background-color: #f8f9fa;
    border-radius: 12rpx;
    border: 1rpx solid #dee2e6;
}

.section-subtitle {
    font-size: 28rpx;
    font-weight: 500;
    color: #495057;
    margin-bottom: 20rpx;
    text-align: center;
}

.mood-table-container {
    background-color: #ffffff;
    border-radius: 8rpx;
    border: 1rpx solid #e9ecef;
    overflow: hidden;
}

.table-row {
    display: flex;
    align-items: stretch;
}

.dates-row {
    background-color: #007aff;
    color: #ffffff;
}

.levels-row {
    background-color: #ffffff;
    border-top: 1rpx solid #e9ecef;
}

.table-cell {
    flex: 1;
    padding: 16rpx 8rpx;
    text-align: center;
    font-size: 24rpx;
    min-height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1rpx solid rgba(0, 0, 0, 0.1);
}

.table-cell:last-child {
    border-right: none;
}

.header-cell {
    font-weight: 500;
    font-size: 26rpx;
    background-color: rgba(0, 0, 0, 0.1);
    color: #ffffff;
    min-width: 80rpx;
}

.levels-row .header-cell {
    background-color: #f8f9fa;
    color: #495057;
    border-right: 1rpx solid #dee2e6;
}

.date-cell {
    font-size: 22rpx;
    font-weight: 400;
    color: #ffffff;
}

.level-cell {
    font-weight: 500;
    color: #6c757d;
    font-size: 28rpx;
}

.level-cell.has-data {
    color: #495057;
    background-color: #e7f3ff;
}

/* 登录提示样式 */
.login-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24rpx;
    padding: 48rpx 32rpx;
}

.prompt-text {
    font-size: 28rpx;
    color: #64748b;
    font-weight: 500;
    letter-spacing: 0.3rpx;
}

.login-btn {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    padding: 24rpx 48rpx;
    border-radius: 16rpx;
    font-size: 28rpx;
    font-weight: 600;
    letter-spacing: 0.5rpx;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4rpx 14rpx rgba(59, 130, 246, 0.25);
    border: none;
}

.login-btn:active {
    transform: translateY(1rpx);
    box-shadow: 0 2rpx 8rpx rgba(59, 130, 246, 0.35);
}

.login-text {
    font-size: 28rpx;
    color: white;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .mood-buttons {
        gap: 8rpx;
    }

    .mood-btn {
        height: 110rpx;
    }

    .mood-icon {
        font-size: 32rpx;
    }

    .mood-desc {
        font-size: 20rpx;
    }

    .table-cell {
        padding: 12rpx 6rpx;
        font-size: 22rpx;
        min-height: 56rpx;
    }
}

@media (max-width: 480rpx) {
    .mood-rating-section {
        padding: 24rpx 16rpx;
    }

    .weekly-mood {
        padding: 20rpx;
    }

    .mood-buttons {
        gap: 6rpx;
    }

    .mood-btn {
        height: 100rpx;
    }

    .mood-icon {
        font-size: 28rpx;
    }

    .mood-desc {
        font-size: 18rpx;
    }

    .table-cell {
        padding: 10rpx 4rpx;
        font-size: 20rpx;
        min-height: 50rpx;
    }
}
</style>
