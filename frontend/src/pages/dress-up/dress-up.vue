<template>
    <view class="dress-up-container">
        <!-- 自定义导航栏 -->
        <view class="custom-navbar">
            <view class="navbar-left" @click="goBack">
                <text class="back-icon">←</text>
            </view>
            <view class="navbar-title">百变小念</view>
            <view class="navbar-right"></view>
        </view>

        <!-- 星星积分显示 -->
        <view class="star-section">
            <view class="star-points-container">
                <view class="star-icon">⭐</view>
                <text class="star-count">{{ starPoints }}</text>
            </view>
        </view>

        <!-- 当前看板娘展示区域 (上1/3) -->
        <view class="mascot-preview-section">
            <!-- <view class="mascot-preview"> -->
            <image :src="currentMascotImage" mode="aspectFit" class="mascot-image" @error="onImageError"></image>
            <!-- </view> -->
            <view class="current-outfit-name">{{ selectedOutfitForPreview ? selectedOutfitForPreview.name :
                currentOutfit.name }}</view>

            <!-- 服装信息和操作按钮 -->
            <view class="outfit-info" v-if="selectedOutfitForPreview">
                <!-- 显示星星成本（仅当用户未拥有该服装时） -->
                <view class="cost-info" v-if="!isOutfitOwned(selectedOutfitForPreview.id)">
                    <view class="cost-container">
                        <view class="cost-star">⭐</view>
                        <text class="cost-text">{{ getOutfitStarCost(selectedOutfitForPreview.id) }}</text>
                    </view>
                </view>

                <!-- 操作按钮 -->
                <view class="action-buttons">
                    <view v-if="isOutfitOwned(selectedOutfitForPreview.id)" class="action-btn switch-btn"
                        @click="switchToOutfit(selectedOutfitForPreview)">
                        切换
                    </view>
                    <view v-else class="action-btn exchange-btn" @click="exchangeOutfit(selectedOutfitForPreview)">
                        兑换
                    </view>
                </view>
            </view>
        </view>

        <!-- 服装选择区域 (下2/3) -->
        <view class="outfits-section">
            <view class="section-title">选择服装</view>
            <view class="outfits-grid">
                <view v-for="outfit in outfits" :key="outfit.id" class="outfit-item"
                    :class="{ active: selectedOutfitForPreview && selectedOutfitForPreview.id === outfit.id }"
                    @click="selectOutfit(outfit)" @longpress="showOutfitDetail(outfit)">
                    <view class="outfit-image-wrapper">
                        <image :src="outfit.mascotImage" mode="aspectFit" class="outfit-image"
                            @error="onOutfitImageError">
                        </image>
                    </view>
                    <view class="outfit-name">{{ outfit.name }}</view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            currentOutfit: {},
            currentMascotImage: '',
            starPoints: 0, // 用户星星积分
            ownedOutfits: [], // 用户拥有的服装列表
            selectedOutfitForPreview: null, // 当前预览的服装（可能未拥有）

            // 服装数据配置
            outfits: [
                {
                    id: 1,
                    name: '默认装',
                    mascotImage: '../../static/outfits/default-full.png'
                },
                {
                    id: 2,
                    name: '红色裙装',
                    mascotImage: '../../static/outfits/red-dress.png'
                },
                {
                    id: 3,
                    name: '恐龙装',
                    mascotImage: '../../static/outfits/dinosaur.png'
                },
                {
                    id: 4,
                    name: '鲨鱼装',
                    mascotImage: '../../static/outfits/shark.png'
                },
                {
                    id: 5,
                    name: '旺仔小乔',
                    mascotImage: '../../static/outfits/wangzaixiaoqiao.png'
                },
                {
                    id: 6,
                    name: '古风少年',
                    mascotImage: '../../static/outfits/Ancient_style_young_man.png'
                },
                {
                    id: 7,
                    name: '蓝猫',
                    mascotImage: '../../static/outfits/Bllue_cat.png'
                },
                {
                    id: 8,
                    name: '妖仙',
                    mascotImage: '../../static/outfits/Demon_Immortal.png'
                },
                {
                    id: 9,
                    name: '北极熊',
                    mascotImage: '../../static/outfits/Polar_bear.png'
                },
                {
                    id: 10,
                    name: '蓝衣少年',
                    mascotImage: '../../static/outfits/The_boy_in_blue.png'
                }
            ]
        }
    },

    onLoad() {
        // 加载用户当前服装
        this.loadCurrentOutfit();

        // 加载用户星星积分
        this.loadStarPoints();

        // 加载用户拥有的服装
        this.loadOwnedOutfits();

        // 设置状态栏样式
        uni.setNavigationBarColor({
            frontColor: '#000000',
            backgroundColor: '#ffffff'
        });
    },

    methods: {
        // 返回Profile页面
        goBack() {
            uni.navigateBack();
        },

        // 加载用户当前服装
        async loadCurrentOutfit() {
            try {
                const token = uni.getStorageSync('access_token');

                if (!token) {
                    // 未登录时使用本地存储
                    this.loadFromLocalStorage();
                    return;
                }

                // 已登录时从服务器获取
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/mascot-outfits/current`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.statusCode === 200 && response.data) {
                    const serverOutfit = response.data;
                    // 在本地服装列表中找到对应的服装
                    const outfit = this.outfits.find(o => o.id === serverOutfit.id);
                    if (outfit) {
                        this.currentOutfit = outfit;
                        this.currentMascotImage = outfit.mascotImage;
                        this.selectedOutfitForPreview = outfit;

                        // 同步到本地存储
                        uni.setStorageSync('selectedOutfit', outfit);
                    } else {
                        // 如果本地没有对应服装，使用默认
                        this.useDefaultOutfit();
                    }
                } else {
                    // 服务器请求失败，使用本地存储
                    this.loadFromLocalStorage();
                }
            } catch (error) {
                console.error('加载当前服装失败:', error);
                // 出错时使用本地存储
                this.loadFromLocalStorage();
            }
        },

        // 从本地存储加载服装
        loadFromLocalStorage() {
            const savedOutfit = uni.getStorageSync('selectedOutfit');
            if (savedOutfit && savedOutfit.id) {
                const outfit = this.outfits.find(o => o.id === savedOutfit.id);
                if (outfit) {
                    this.currentOutfit = outfit;
                    this.currentMascotImage = outfit.mascotImage;
                    this.selectedOutfitForPreview = outfit;
                } else {
                    this.useDefaultOutfit();
                }
            } else {
                this.useDefaultOutfit();
            }
        },

        // 使用默认服装
        useDefaultOutfit() {
            this.currentOutfit = this.outfits[0];
            this.currentMascotImage = this.currentOutfit.mascotImage;
            this.selectedOutfitForPreview = this.currentOutfit;
        },

        // 选择服装（仅预览，不保存）
        selectOutfit(outfit) {
            // 立即更新预览图
            this.selectedOutfitForPreview = outfit;
            this.currentMascotImage = outfit.mascotImage;

            // 添加选择效果
            uni.vibrateShort();
        },

        // 图片加载错误处理
        onImageError(e) {
            console.error('看板娘图片加载失败:', e);
            // 使用默认图片
            this.currentMascotImage = '../../static/outfits/default-full.png';
        },

        onOutfitImageError(e) {
            console.error('服装图片加载失败:', e);
        },

        // 加载用户星星积分
        async loadStarPoints() {
            const token = uni.getStorageSync('access_token');
            if (!token) {
                this.starPoints = 0;
                return;
            }

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/star-points/balance`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.statusCode === 200) {
                    this.starPoints = response.data.current_points || 0;
                } else if (response.statusCode === 401) {
                    // Token过期
                    this.starPoints = 0;
                }
            } catch (error) {
                console.error('获取星星积分失败:', error);
                this.starPoints = 0;
            }
        },

        // 加载用户拥有的服装
        async loadOwnedOutfits() {
            const token = uni.getStorageSync('access_token');
            if (!token) {
                this.ownedOutfits = [1]; // 未登录时只拥有默认装
                return;
            }

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/mascot-outfits/user-outfits`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.statusCode === 200) {
                    // 从服务器响应中提取用户拥有的服装ID
                    this.ownedOutfits = response.data
                        .filter(outfit => outfit.purchased_at) // 检查purchased_at字段
                        .map(outfit => outfit.id);

                    // 确保默认装总是被拥有
                    if (!this.ownedOutfits.includes(1)) {
                        this.ownedOutfits.push(1);
                    }
                } else {
                    this.ownedOutfits = [1]; // 默认只拥有默认装
                }
            } catch (error) {
                console.error('获取拥有服装失败:', error);
                this.ownedOutfits = [1]; // 默认只拥有默认装
            }
        },

        // 检查用户是否拥有某个服装
        isOutfitOwned(outfitId) {
            return this.ownedOutfits.includes(outfitId);
        },

        // 获取服装星星成本
        getOutfitStarCost(outfitId) {
            const costs = {
                1: 0,    // 默认装
                2: 100,  // 红色裙装
                3: 150,  // 恐龙装
                4: 200,  // 鲨鱼装
                5: 250,  // 旺仔小乔
                6: 300,  // 古风少年
                7: 280,  // 蓝猫
                8: 400,  // 妖仙
                9: 350,  // 北极熊
                10: 320  // 蓝衣少年
            };
            return costs[outfitId] || 0;
        },

        // 切换到已拥有的服装
        async switchToOutfit(outfit) {
            if (!this.isOutfitOwned(outfit.id)) {
                uni.showToast({
                    title: '您还未拥有此服装',
                    icon: 'none'
                });
                return;
            }

            // 更新当前服装
            this.currentOutfit = outfit;

            // 保存到本地存储
            uni.setStorageSync('selectedOutfit', outfit);

            // 同步到服务器
            const token = uni.getStorageSync('access_token');
            if (token) {
                try {
                    await uni.request({
                        url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/mascot-outfits/set-current`,
                        method: 'POST',
                        header: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        data: {
                            outfit_id: outfit.id
                        }
                    });
                } catch (error) {
                    console.error('同步服装失败:', error);
                }
            }

            uni.showToast({
                title: `已切换到：${outfit.name}`,
                icon: 'success',
                duration: 1500
            });
        },

        // 兑换服装
        async exchangeOutfit(outfit) {
            const cost = this.getOutfitStarCost(outfit.id);

            if (this.starPoints < cost) {
                uni.showToast({
                    title: `星星不足，需要 ${cost} 个星星`,
                    icon: 'none'
                });
                return;
            }

            // 确认兑换
            uni.showModal({
                title: '确认兑换',
                content: `确定花费 ${cost} 个星星兑换 ${outfit.name} 吗？`,
                success: async (res) => {
                    if (res.confirm) {
                        await this.performExchange(outfit);
                    }
                }
            });
        },

        // 执行兑换
        async performExchange(outfit) {
            const token = uni.getStorageSync('access_token');
            if (!token) {
                uni.showToast({
                    title: '请先登录',
                    icon: 'none'
                });
                return;
            }

            try {
                const response = await uni.request({
                    url: `${process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000'}/mascot-outfits/purchase/${outfit.id}`,
                    method: 'POST',
                    header: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.statusCode === 200) {
                    // 兑换成功，更新本地数据
                    this.ownedOutfits.push(outfit.id);

                    // 使用服务器返回的最新积分
                    if (response.data && response.data.remaining_points !== undefined) {
                        this.starPoints = response.data.remaining_points;
                    } else {
                        // 如果服务器没有返回积分信息，重新加载
                        this.loadStarPoints();
                    }

                    uni.showToast({
                        title: `${outfit.name} 兑换成功！`,
                        icon: 'success',
                        duration: 2000
                    });

                    // 自动切换到新兑换的服装
                    setTimeout(() => {
                        this.switchToOutfit(outfit);
                    }, 1000);
                } else {
                    uni.showToast({
                        title: '兑换失败，请重试',
                        icon: 'none'
                    });
                }
            } catch (error) {
                console.error('兑换服装失败:', error);
                uni.showToast({
                    title: '兑换失败，请重试',
                    icon: 'none'
                });
            }
        },

        // 显示服装详情
        showOutfitDetail(outfit) {
            uni.vibrateShort();
            uni.showModal({
                title: outfit.name,
                content: `这是${outfit.name}套装。点击"确定"立即换装，或点击"取消"继续浏览。`,
                confirmText: '立即换装',
                cancelText: '取消',
                success: (res) => {
                    if (res.confirm) {
                        this.selectOutfit(outfit);
                    }
                }
            });
        }
    }
}
</script>

<style scoped>
.dress-up-container {
    width: 100%;
    min-height: 100vh;
    background: #faf8f3;
    position: relative;
}

/* 自定义导航栏 */
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 88rpx;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    padding: 0 32rpx;
    z-index: 1000;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.navbar-left {
    flex: 0 0 80rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 30rpx;
    background: rgba(102, 126, 234, 0.1);
    transition: all 0.3s ease;
}

.navbar-left:active {
    background: rgba(102, 126, 234, 0.2);
    transform: scale(0.95);
}

.back-icon {
    font-size: 32rpx;
    color: #667eea;
    font-weight: bold;
}

.navbar-title {
    flex: 1;
    text-align: center;
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
}

.navbar-right {
    flex: 0 0 80rpx;
}

/* 星星积分区域 */
.star-section {
    margin-top: 88rpx;
    padding: 20rpx 30rpx;
    background: rgba(255, 255, 255, 0.95);
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.star-points-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8rpx;
    background: linear-gradient(135deg, #ffd700, #ffed4e);
    border: 2rpx solid #f0c400;
    border-radius: 25rpx;
    padding: 15rpx 25rpx;
    margin: 0 auto;
    max-width: 200rpx;
    box-shadow: 0 4rpx 12rpx rgba(255, 215, 0, 0.3);
    transition: all 0.3s ease;
}

.star-points-container:active {
    transform: translateY(1rpx);
    box-shadow: 0 2rpx 8rpx rgba(255, 215, 0, 0.4);
}

.star-icon {
    font-size: 32rpx;
    line-height: 1;
}

.star-count {
    font-size: 30rpx;
    font-weight: bold;
    color: #b8860b;
    line-height: 1;
}

.star-label {
    font-size: 24rpx;
    color: #b8860b;
    line-height: 1;
}

/* 看板娘预览区域 */
.mascot-preview-section {
    height: 55vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20rpx 20rpx 20rpx;
}

.mascot-preview {
    width: 300rpx;
    height: 300rpx;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 150rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20rpx 40rpx rgba(0, 0, 0, 0.2);
    overflow: hidden;
    transition: all 0.3s ease;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10rpx);
    }
}

.mascot-image {
    width: 500rpx;
    height: 500rpx;
    border-radius: 0;
}

.current-outfit-name {
    margin-top: 30rpx;
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

/* 服装信息和操作区域 */
.outfit-info {
    margin-top: 20rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15rpx;
}

.cost-info {
    display: flex;
    justify-content: center;
}

.cost-container {
    display: flex;
    align-items: center;
    gap: 5rpx;
    background: rgba(255, 215, 0, 0.2);
    border: 1rpx solid #ffd700;
    border-radius: 20rpx;
    padding: 8rpx 16rpx;
}

.cost-star {
    font-size: 24rpx;
}

.cost-text {
    font-size: 24rpx;
    font-weight: bold;
    color: #b8860b;
}

.action-buttons {
    display: flex;
    justify-content: center;
}

.action-btn {
    padding: 12rpx 30rpx;
    border-radius: 25rpx;
    font-size: 26rpx;
    font-weight: bold;
    text-align: center;
    transition: all 0.3s ease;
    min-width: 120rpx;
}

.switch-btn {
    background: linear-gradient(135deg, #67c23a, #85ce61);
    color: #fff;
    box-shadow: 0 4rpx 12rpx rgba(103, 194, 58, 0.3);
}

.switch-btn:active {
    transform: translateY(1rpx);
    box-shadow: 0 2rpx 8rpx rgba(103, 194, 58, 0.4);
}

.exchange-btn {
    background: linear-gradient(135deg, #409eff, #67c23a);
    color: #fff;
    box-shadow: 0 4rpx 12rpx rgba(64, 158, 255, 0.3);
}

.exchange-btn:active {
    transform: translateY(1rpx);
    box-shadow: 0 2rpx 8rpx rgba(64, 158, 255, 0.4);
}

/* 服装选择区域 */
.outfits-section {
    flex: 1;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 40rpx 40rpx 0 0;
    padding: 40rpx 30rpx;
    min-height: 10vh;
}

.section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 30rpx;
    text-align: center;
}

.outfits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160rpx, 1fr));
    gap: 30rpx;
    padding-bottom: 40rpx;
}

/* 移动端优化 */
@media (max-width: 750px) {
    .outfits-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* 桌面端优化 */
@media (min-width: 1024px) {
    .outfits-grid {
        grid-template-columns: repeat(5, 1fr);
        max-width: 1000rpx;
        margin: 0 auto;
    }
}

.outfit-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx;
    border-radius: 20rpx;
    background: #fff;
    box-shadow: 0 8rpx 16rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}

.outfit-item:active {
    transform: translateY(4rpx) scale(0.95);
}

.outfit-item:hover {
    transform: translateY(-2rpx);
    box-shadow: 0 12rpx 24rpx rgba(0, 0, 0, 0.15);
}

.outfit-item.active {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    box-shadow: 0 12rpx 24rpx rgba(102, 126, 234, 0.3);
}

.outfit-image-wrapper {
    width: 100rpx;
    height: 100rpx;
    border-radius: 16rpx;
    overflow: hidden;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
}

.outfit-image {
    width: 100%;
    height: 100%;
}

.outfit-name {
    margin-top: 16rpx;
    font-size: 24rpx;
    text-align: center;
    line-height: 1.3;
}

.outfit-item.active .outfit-name {
    color: #fff;
    font-weight: bold;
}

/* 响应式调整 */
@media (max-width: 480px) {
    .mascot-preview {
        width: 250rpx;
        height: 250rpx;
    }

    .mascot-image {
        width: 380rpx;
        height: 380rpx;
    }

    .outfits-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20rpx;
    }

    .outfit-item {
        padding: 15rpx;
    }

    .outfit-image-wrapper {
        width: 80rpx;
        height: 80rpx;
        border-radius: 12rpx;
    }

    .outfit-name {
        font-size: 22rpx;
    }
}
</style>
