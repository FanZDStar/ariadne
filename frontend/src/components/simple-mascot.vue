<!-- filepath: pages/components/simple-mascot.vue -->
<template>
    <view class="mascot-container">
        <!-- 看板娘主体 -->
        <view class="mascot" :class="currentAction" :style="{ left: position.x + 'px', top: position.y + 'px' }"
            @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd" @tap="handleTap">
            <image class="mascot-image" :src="currentImage" mode="aspectFit"></image>
        </view>

        <!-- 对话气泡 -->
        <view v-if="showBubble" class="speech-bubble" :style="bubbleStyle">
            {{ currentSpeech }}
        </view>

        <!-- 换装弹窗 -->
        <view v-if="showDressUp" class="dress-modal" @tap="closeDressUp">
            <view class="dress-content" @tap.stop>
                <view class="dress-title">换装</view>
                <view class="outfit-list">
                    <view v-for="outfit in outfits" :key="outfit.id" class="outfit-item" @tap="changeOutfit(outfit)">
                        <image :src="outfit.preview" mode="aspectFit"></image>
                        <text>{{ outfit.name }}</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            position: { x: 300, y: 500 },
            isDragging: false,
            startTouch: { x: 0, y: 0 },
            currentAction: 'idle',
            currentImage: '/static/mascot/idle.png',
            showBubble: false,
            currentSpeech: '',
            showDressUp: false,
            wanderTimer: null,

            // 动作配置
            actions: [
                { name: 'idle', image: '/static/mascot/idle.png' },
                { name: 'wave', image: '/static/mascot/wave.png' },
                { name: 'happy', image: '/static/mascot/happy.png' },
                { name: 'sleep', image: '/static/mascot/sleep.png' }
            ],

            // 对话内容
            speeches: [
                '你好呀~', '今天心情不错呢!', '要试试新衣服吗?',
                '点击我换装哦~', '我在这里陪你呢!'
            ],

            // 服装配置
            outfits: [
                {
                    id: 1, name: '默认', preview: '/static/outfits/default.png', images: {
                        idle: '/static/mascot/idle.png',
                        wave: '/static/mascot/wave.png'
                    }
                },
                {
                    id: 2, name: '夏装', preview: '/static/outfits/summer.png', images: {
                        idle: '/static/mascot/summer-idle.png',
                        wave: '/static/mascot/summer-wave.png'
                    }
                }
            ]
        }
    },

    computed: {
        bubbleStyle() {
            return {
                left: (this.position.x + 100) + 'px',
                top: (this.position.y - 50) + 'px'
            }
        }
    },

    mounted() {
        this.startWandering();
    },

    methods: {
        // 拖拽处理
        handleTouchStart(e) {
            this.isDragging = true;
            this.startTouch.x = e.touches[0].clientX - this.position.x;
            this.startTouch.y = e.touches[0].clientY - this.position.y;
        },

        handleTouchMove(e) {
            if (!this.isDragging) return;
            e.preventDefault();

            this.position.x = e.touches[0].clientX - this.startTouch.x;
            this.position.y = e.touches[0].clientY - this.startTouch.y;

            // 边界检查
            this.position.x = Math.max(0, Math.min(this.position.x, uni.getSystemInfoSync().windowWidth - 100));
            this.position.y = Math.max(0, Math.min(this.position.y, uni.getSystemInfoSync().windowHeight - 120));
        },

        handleTouchEnd() {
            this.isDragging = false;
        },

        // 点击交互
        handleTap() {
            if (this.isDragging) return;

            // 长按进入换装，短按切换动作
            setTimeout(() => {
                if (!this.showDressUp) {
                    this.playRandomAction();
                    this.showSpeech();
                }
            }, 100);
        },

        // 播放随机动作
        playRandomAction() {
            const randomAction = this.actions[Math.floor(Math.random() * this.actions.length)];
            this.currentAction = randomAction.name;
            this.currentImage = randomAction.image;

            // 2秒后回到idle状态
            setTimeout(() => {
                this.currentAction = 'idle';
                this.currentImage = this.actions[0].image;
            }, 2000);
        },

        // 显示对话
        showSpeech() {
            this.currentSpeech = this.speeches[Math.floor(Math.random() * this.speeches.length)];
            this.showBubble = true;

            setTimeout(() => {
                this.showBubble = false;
            }, 3000);
        },

        // 自动闲逛
        startWandering() {
            this.wanderTimer = setInterval(() => {
                if (!this.isDragging && Math.random() < 0.5) {
                    this.autoWander();
                }
            }, 1000);
        },

        autoWander() {
            const systemInfo = uni.getSystemInfoSync();
            const targetX = Math.random() * (systemInfo.windowWidth - 100);
            const targetY = Math.random() * (systemInfo.windowHeight - 120);

            // 简单的移动动画
            const startX = this.position.x;
            const startY = this.position.y;
            const duration = 2000;
            const startTime = Date.now();

            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);

                this.position.x = startX + (targetX - startX) * progress;
                this.position.y = startY + (targetY - startY) * progress;

                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            };

            animate();
        },

        // 换装相关
        openDressUp() {
            this.showDressUp = true;
        },

        closeDressUp() {
            this.showDressUp = false;
        },

        changeOutfit(outfit) {
            // 更新所有动作的图片
            this.actions = this.actions.map(action => ({
                ...action,
                image: outfit.images[action.name] || action.image
            }));

            // 更新当前图片
            this.currentImage = outfit.images.idle;
            this.closeDressUp();

            this.showSpeech();
            this.currentSpeech = '新衣服很好看吧~';
        }
    },

    // 长按事件（进入换装）
    onLongpress() {
        this.openDressUp();
    },

    beforeDestroy() {
        if (this.wanderTimer) {
            clearInterval(this.wanderTimer);
        }
    }
}
</script>

<style scoped>
.mascot-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 9999;
}

.mascot {
    position: absolute;
    width: 100px;
    height: 120px;
    pointer-events: auto;
    transition: transform 0.3s ease;
}

.mascot.wave {
    animation: wave 0.5s ease-in-out;
}

.mascot.happy {
    animation: bounce 0.6s ease-in-out;
}

.mascot-image {
    width: 100%;
    height: 100%;
}

.speech-bubble {
    position: absolute;
    background: #fff;
    border: 2px solid #ff69b4;
    border-radius: 20px;
    padding: 10px 15px;
    font-size: 14px;
    color: #333;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    pointer-events: none;
    animation: fadeInOut 3s ease-in-out;
}

.speech-bubble::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 20px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-top-color: #ff69b4;
}

.dress-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: auto;
}

.dress-content {
    background: white;
    border-radius: 15px;
    padding: 20px;
    width: 80%;
    max-width: 400px;
}

.dress-title {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
}

.outfit-list {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}

.outfit-item {
    flex: 1;
    min-width: 80px;
    text-align: center;
    padding: 10px;
    border: 2px solid #eee;
    border-radius: 10px;
}

.outfit-item image {
    width: 50px;
    height: 60px;
    margin-bottom: 5px;
}

.outfit-item text {
    font-size: 12px;
    color: #666;
}

@keyframes wave {

    0%,
    100% {
        transform: rotate(0deg);
    }

    25% {
        transform: rotate(-10deg);
    }

    75% {
        transform: rotate(10deg);
    }
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

@keyframes fadeInOut {

    0%,
    100% {
        opacity: 0;
    }

    20%,
    80% {
        opacity: 1;
    }
}
</style>