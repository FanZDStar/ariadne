<template>
    <view class="back-to-top-container">
        <view class="back-to-top-btn" :class="{ 'show': showButton }" @click="scrollToTop"
            :style="{ bottom: bottom + 'rpx', right: right + 'rpx' }">
            <text class="back-to-top-icon">{{ icon }}</text>
        </view>
    </view>
</template>

<script>
export default {
    name: 'BackToTop',
    props: {
        // 显示阈值，滚动超过多少像素显示按钮
        threshold: {
            type: Number,
            default: 30
        },
        // 按钮距离底部的距离
        bottom: {
            type: Number,
            default: 40
        },
        // 按钮距离右边的距离
        right: {
            type: Number,
            default: 40
        },
        // 按钮图标
        icon: {
            type: String,
            default: '↑'
        },
        // 滚动动画持续时间
        duration: {
            type: Number,
            default: 100
        },
        // 自定义样式类名
        customClass: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            showButton: false
        }
    },
    mounted() {
        // 在组件挂载时开始监听滚动
        this.startScrollListener();
    },
    beforeDestroy() {
        // 组件销毁前移除监听
        this.removeScrollListener();
    },
    methods: {
        startScrollListener() {
            // 由于 uni-app 的页面滚动监听是在页面级别的，
            // 我们需要通过事件总线或其他方式来处理
            // 这里提供一个简单的实现
            this.scrollHandler = (scrollTop) => {
                this.showButton = scrollTop > this.threshold;
            };

            // 触发父组件开始监听滚动
            this.$emit('start-scroll-listener', this.scrollHandler);
        },

        removeScrollListener() {
            this.$emit('remove-scroll-listener');
        },

        scrollToTop() {
            uni.pageScrollTo({
                scrollTop: 0,
                duration: this.duration,
                success: () => {
                    this.$emit('scroll-to-top-success');
                },
                fail: () => {
                    this.$emit('scroll-to-top-fail');
                }
            });
        },

        // 提供外部调用的方法来更新显示状态
        updateShowState(scrollTop) {
            this.showButton = scrollTop > this.threshold;
        }
    }
}
</script>

<style scoped>
.back-to-top-container {
    position: fixed;
    z-index: 999;
    pointer-events: none;
}

.back-to-top-btn {
    position: fixed;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    width: 100rpx;
    height: 100rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
    transform: translateY(200rpx);
    opacity: 0;
    pointer-events: none;
}

.back-to-top-btn.show {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
    animation: float 3s ease-in-out infinite;
}

.back-to-top-btn:active {
    transform: scale(0.95);
}

.back-to-top-icon {
    font-size: 32rpx;
    font-weight: bold;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-8rpx);
    }
}

/* 自定义主题样式 */
.back-to-top-btn.theme-simple {
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(10rpx);
}

.back-to-top-btn.theme-colorful {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    background-size: 400% 400%;
    animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}
</style>