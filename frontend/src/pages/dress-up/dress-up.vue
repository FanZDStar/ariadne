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

        <!-- 当前看板娘展示区域 (上1/3) -->
        <view class="mascot-preview-section">
            <!-- <view class="mascot-preview"> -->
            <image :src="currentMascotImage" mode="aspectFit" class="mascot-image" @error="onImageError"></image>
            <!-- </view> -->
            <view class="current-outfit-name">{{ currentOutfit.name }}</view>
        </view>

        <!-- 服装选择区域 (下2/3) -->
        <view class="outfits-section">
            <view class="section-title">选择服装</view>
            <view class="outfits-grid">
                <view v-for="outfit in outfits" :key="outfit.id" class="outfit-item"
                    :class="{ active: currentOutfit.id === outfit.id }" @click="selectOutfit(outfit)"
                    @longpress="showOutfitDetail(outfit)">
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
                }
            ]
        }
    },

    onLoad() {
        // 从本地存储恢复上次选择的服装
        const savedOutfit = uni.getStorageSync('selectedOutfit');
        if (savedOutfit && savedOutfit.id) {
            const outfit = this.outfits.find(o => o.id === savedOutfit.id);
            if (outfit) {
                this.currentOutfit = outfit;
                this.currentMascotImage = outfit.mascotImage;
            } else {
                // 如果保存的服装不存在，使用默认服装
                this.currentOutfit = this.outfits[0];
                this.currentMascotImage = this.currentOutfit.mascotImage;
            }
        } else {
            // 设置默认服装
            this.currentOutfit = this.outfits[0];
            this.currentMascotImage = this.currentOutfit.mascotImage;
        }

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

        // 选择服装
        selectOutfit(outfit) {
            if (this.currentOutfit.id === outfit.id) return; // 避免重复选择

            this.currentOutfit = outfit;
            this.currentMascotImage = outfit.mascotImage;

            // 保存选择的服装到本地存储
            uni.setStorageSync('selectedOutfit', outfit);

            // 添加选择效果
            uni.vibrateShort();

            // 显示选择成功提示
            uni.showToast({
                title: `已换装：${outfit.name}`,
                icon: 'success',
                duration: 1500
            });
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

/* 看板娘预览区域 */
.mascot-preview-section {
    margin-top: 88rpx;
    height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40rpx 20rpx 20rpx;
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
    border-radius: 250rpx;
}

.current-outfit-name {
    margin-top: 30rpx;
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
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
