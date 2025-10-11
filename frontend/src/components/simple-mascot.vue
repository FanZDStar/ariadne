<!-- filepath: pages/components/simple-mascot.vue -->
<template>
  <view class="mascot-container">
    <!-- 看板娘主体 -->
    <view class="mascot" :class="currentAction" :style="{ left: position.x + 'px', top: position.y + 'px' }"
      @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd" @tap="handleTap">
      <!-- 静态小人图片 -->
      <image v-if="!isPlayingAnimation" class="mascot-image" :src="currentImage" mode="aspectFit"></image>
      <!-- Lottie动画容器 -->
      <view v-if="isPlayingAnimation" class="lottie-container" :id="lottieContainerId"></view>
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
// 引入lottie-web
import lottie from "lottie-web";

export default {
  data() {
    return {
      position: { x: 300, y: 500 },
      isDragging: false,
      startTouch: { x: 0, y: 0 },
      currentAction: "idle",
      currentImage: "/static/outfits/default-full.png",
      showBubble: false,
      currentSpeech: "",
      showDressUp: false,

      // Lottie动画相关
      isPlayingAnimation: false,
      lottieInstance: null,
      lottieContainerId: "lottie-" + Date.now(),
      actionTimer: null,

      // 动画文件缓存
      animationCache: {}, // 缓存已检查的动画文件状态

      outfitCheckTimer: null,
      lastOutfitId: null, // 记录上次的服装ID，用于检测变化
      currentOutfitId: 1, // 当前小人ID

      // 不同小人的动作组配置（与换装系统ID统一）
      outfitActionGroups: {
        1: {
          // 默认装
          name: "默认装",
          staticImage: "/static/outfits/default-full.png",
          actionCount: 3, // 动作数量
          speeches: ["你好呀~", "今天心情不错呢!", "我来跟你打招呼!"],
        },
        2: {
          // 红色裙装
          name: "红色裙装",
          staticImage: "/static/outfits/red-dress.png",
          actionCount: 2,
          speeches: [
            "这条裙子很漂亮吧~",
            "红色是我的幸运色!",
            "今天穿得特别美!",
          ],
        },
        3: {
          // 恐龙装
          name: "恐龙装",
          staticImage: "/static/outfits/dinosaur.png",
          actionCount: 2,
          speeches: ["恐龙时代来啦~", "ROAR! 我是小恐龙!", "穿越到侏罗纪!"],
        },
        4: {
          // 鲨鱼装
          name: "鲨鱼装",
          staticImage: "/static/outfits/shark.png",
          actionCount: 1,
          speeches: ["游向深海~", "我是海洋之王!", "鲨鱼出没注意!"],
        },
        5: {
          // 旺仔小乔
          name: "旺仔小乔",
          staticImage: "/static/outfits/wangzaixiaoqiao.png",
          actionCount: 1,
          speeches: ["旺仔牛奶真好喝~", "小乔来啦!", "甜甜的味道!"],
        },
      },

      // 对话内容
      speeches: [
        "你好呀~",
        "今天心情不错呢!",
        "要试试新衣服吗?",
        "点击我换装哦~",
        "我在这里陪你呢!",
      ],
    };
  },

  computed: {
    bubbleStyle() {
      return {
        left: this.position.x + 100 + "px",
        top: this.position.y - 50 + "px",
      };
    },
  },

  mounted() {
    this.checkPosition();
    this.checkOutfitStorage();

    // 强制清除所有动画缓存
    this.animationCache = {};

    // 开始随机动作定时器
    this.startRandomActions();

    // 监听服装变化
    this.outfitCheckTimer = setInterval(() => {
      this.checkOutfitStorage();
    }, 2000);
  },

  onLoad() {
    // 页面加载时加载服装设置
    this.loadSavedOutfit();
  },

  onShow() {
    // 页面显示时重新加载服装设置
    this.loadSavedOutfit();
  },

  onReady() {
    // 页面渲染完成时检查服装
    this.loadSavedOutfit();
  },

  beforeDestroy() {
    // 清理定时器和Lottie实例
    this.clearAllTimers();
    this.clearLottieInstance();
  },

  methods: {
    // 检查位置边界
    checkPosition() {
      // 获取屏幕尺寸
      const systemInfo = uni.getSystemInfoSync();
      const maxX = systemInfo.windowWidth - 130; // 减去小人宽度
      const maxY = systemInfo.windowHeight - 156; // 减去小人高度

      if (this.position.x > maxX) this.position.x = maxX;
      if (this.position.y > maxY) this.position.y = maxY;
      if (this.position.x < 0) this.position.x = 0;
      if (this.position.y < 0) this.position.y = 0;
    },

    // 检查服装存储
    async checkOutfitStorage() {
      // 先尝试从服务器同步
      await this.syncOutfitFromServer();

      const savedOutfit = uni.getStorageSync("selectedOutfit");

      if (savedOutfit && savedOutfit.mascotImage) {
        const outfitId = savedOutfit.id || 1;

        // 检查是否有服装变化
        if (this.lastOutfitId !== outfitId) {
          this.currentOutfitId = outfitId;
          this.currentImage = savedOutfit.mascotImage;
          this.lastOutfitId = outfitId;

          // 清除动画缓存，强制重新检查可用动作
          const cacheKey = `character_${outfitId}`;
          delete this.animationCache[cacheKey];

          // 更新当前小人的语音
          this.updateCurrentSpeech();
        }
      } else {
        // 使用默认小人
        if (this.currentOutfitId !== 1) {
          this.currentOutfitId = 1;
          this.currentImage = "/static/outfits/default-full.png";
          this.lastOutfitId = 1;
          this.updateCurrentSpeech();
        }
      }
    },

    // 更新当前语音内容
    updateCurrentSpeech() {
      const currentOutfit = this.outfitActionGroups[this.currentOutfitId];
      if (currentOutfit && currentOutfit.speeches) {
        this.speeches = currentOutfit.speeches;
      }
    },

    // 开始随机动作
    startRandomActions() {
      this.scheduleNextAction();
    },

    // 安排下一个动作
    scheduleNextAction() {
      // 5-10秒随机间隔
      const interval = Math.random() * 5000 + 5000;
      this.actionTimer = setTimeout(() => {
        this.playRandomAction();
        this.scheduleNextAction(); // 继续安排下一个动作
      }, interval);
    },

    // 播放随机动作
    playRandomAction() {
      const currentOutfit = this.outfitActionGroups[this.currentOutfitId];

      if (!currentOutfit || currentOutfit.actionCount === 0) {
        return;
      }

      // 检查并获取可用的动作
      this.getAvailableActions().then((availableActions) => {
        if (availableActions.length === 0) {
          return;
        }

        // 从可用动作中随机选择
        const randomIndex = Math.floor(Math.random() * availableActions.length);
        const actionNumber = availableActions[randomIndex];

        this.playLottieAction(actionNumber);
      });
    },

    // 获取当前角色可用的动作列表
    async getAvailableActions() {
      const currentOutfit = this.outfitActionGroups[this.currentOutfitId];
      if (!currentOutfit) return [];

      const cacheKey = `character_${this.currentOutfitId}`;

      // 如果缓存中有数据，直接返回
      if (this.animationCache[cacheKey]) {
        return this.animationCache[cacheKey];
      }

      const availableActions = [];

      // 检查每个动作文件是否存在且有效
      for (let i = 1; i <= currentOutfit.actionCount; i++) {
        const animationPath = `/src/static/animations/${this.currentOutfitId}/${i}/data.json`;

        try {
          // 先检查文件是否存在
          const response = await fetch(animationPath);
          if (response.ok) {
            // 检查文件内容是否有效
            const text = await response.text();
            if (text.trim() && text.trim() !== "") {
              try {
                // 尝试解析 JSON 来验证格式
                const jsonData = JSON.parse(text);
                if (jsonData && typeof jsonData === "object") {
                  availableActions.push(i);
                }
              } catch (parseError) {
                // JSON解析失败，跳过此文件
              }
            }
          }
        } catch (error) {
          // 文件访问失败，跳过此文件
        }
      }

      // 缓存结果
      this.animationCache[cacheKey] = availableActions;
      return availableActions;
    },

    // 播放Lottie动作
    playLottieAction(actionNumber) {
      if (this.isPlayingAnimation) {
        return; // 如果正在播放动画，跳过
      }

      // 构建动画文件路径: animations/角色ID/动作编号/data.json
      const animationPath = `/src/static/animations/${this.currentOutfitId}/${actionNumber}/data.json`;

      this.loadAndPlayLottie(animationPath);
    },
    // 加载并播放Lottie动画
    async loadAndPlayLottie(animationPath) {
      this.isPlayingAnimation = true;

      // 获取Lottie容器
      const containerId = this.lottieContainerId;

      this.$nextTick(async () => {
        if (lottie && this.isPlayingAnimation) {
          try {
            // 清理之前的实例
            this.clearLottieInstance();

            // 先尝试直接使用path方式
            this.lottieInstance = lottie.loadAnimation({
              container: document.getElementById(containerId),
              renderer: "svg",
              loop: false,
              autoplay: true,
              path: animationPath,
            });

            // 监听动画完成
            this.lottieInstance.addEventListener("complete", () => {
              this.onAnimationComplete();
            });

            // 监听加载错误
            this.lottieInstance.addEventListener(
              "data_failed",
              async (error) => {
                // 方案B: 手动加载并修改数据
                try {
                  const response = await fetch(animationPath);
                  if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                  }

                  let animationData = await response.json();

                  // 修改assets中的图片路径
                  if (animationData.assets) {
                    const basePath = animationPath.replace("/data.json", "/");
                    animationData.assets.forEach((asset) => {
                      if (asset.u && asset.p) {
                        // 将相对路径转换为绝对路径
                        asset.u = basePath + asset.u;
                      }
                    });
                  }

                  // 清理失败的实例
                  this.clearLottieInstance();

                  // 使用修改后的数据重新创建实例
                  this.lottieInstance = lottie.loadAnimation({
                    container: document.getElementById(containerId),
                    renderer: "svg",
                    loop: false,
                    autoplay: true,
                    animationData: animationData,
                  });

                  // 重新绑定事件
                  this.lottieInstance.addEventListener("complete", () => {
                    this.onAnimationComplete();
                  });
                } catch (backupError) {
                  this.onAnimationComplete();
                }
              }
            );

            // 添加超时处理，防止无限等待
            setTimeout(() => {
              if (this.isPlayingAnimation && this.lottieInstance) {
                this.onAnimationComplete();
              }
            }, 10000); // 延长超时时间到10秒
          } catch (error) {
            this.onAnimationComplete();
          }
        } else {
          this.onAnimationComplete();
        }
      });
    },

    // 动画完成回调
    onAnimationComplete() {
      this.isPlayingAnimation = false;
      this.clearLottieInstance();
    },

    // 清理Lottie实例
    clearLottieInstance() {
      if (this.lottieInstance) {
        this.lottieInstance.destroy();
        this.lottieInstance = null;
      }
    },

    // 清理所有定时器
    clearAllTimers() {
      if (this.actionTimer) {
        clearTimeout(this.actionTimer);
        this.actionTimer = null;
      }
      if (this.outfitCheckTimer) {
        clearInterval(this.outfitCheckTimer);
        this.outfitCheckTimer = null;
      }
    },

    // 从服务器同步服装设置
    async syncOutfitFromServer() {
      const token = uni.getStorageSync('access_token');
      if (!token) return; // 未登录时不同步

      try {
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
          const localOutfit = {
            id: serverOutfit.id,
            name: serverOutfit.name,
            mascotImage: serverOutfit.mascot_image
          };

          // 更新本地存储
          uni.setStorageSync('selectedOutfit', localOutfit);

          console.log('从服务器同步服装设置:', localOutfit);
        }
      } catch (error) {
        console.error('从服务器同步服装失败:', error);
      }
    },

    // 加载保存的服装设置
    async loadSavedOutfit() {
      // 先尝试从服务器同步
      await this.syncOutfitFromServer();

      const savedOutfit = uni.getStorageSync("selectedOutfit");
      if (savedOutfit && savedOutfit.mascotImage) {
        // 检查是否有服装变化
        const isFirstLoad =
          this.lastOutfitId === null &&
          this.currentImage === "/static/outfits/default-full.png";

        if (this.lastOutfitId !== savedOutfit.id) {
          this.currentImage = savedOutfit.mascotImage;
          this.lastOutfitId = savedOutfit.id;

          // 只有在非首次加载时才显示换装效果
          if (!isFirstLoad) {
            this.playOutfitChangeEffect();
          }
        }
      } else {
        // 如果没有保存的服装，使用默认图片
        if (this.currentImage !== "/static/outfits/default-full.png") {
          this.currentImage = "/static/outfits/default-full.png";
          this.lastOutfitId = null;
        }
      }
    },

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

      // 边界检查 - 使用新的尺寸
      const systemInfo = uni.getSystemInfoSync();
      this.position.x = Math.max(
        0,
        Math.min(this.position.x, systemInfo.windowWidth - 130)
      );
      this.position.y = Math.max(
        0,
        Math.min(this.position.y, systemInfo.windowHeight - 156)
      );
    },

    handleTouchEnd() {
      this.isDragging = false;
    },

    // 点击交互
    handleTap() {
      if (this.isDragging) return;

      // 短按触发动作和语音
      setTimeout(() => {
        if (!this.showDressUp) {
          this.playRandomAction();
          this.showSpeech();
        }
      }, 100);
    },

    // 长按打开换装界面
    handleLongPress() {
      this.showDressUp = true;
    },

    // 测试方法：检查当前角色所有动画
    async checkCurrentCharacterAnimations() {
      const availableActions = await this.getAvailableActions();

      if (availableActions.length === 0) {
        console.warn(`角色 ${this.currentOutfitId} 没有可用的动画文件`);
      }

      return availableActions;
    }, // 显示对话
    showSpeech() {
      const currentOutfit = this.outfitActionGroups[this.currentOutfitId];
      const speeches = currentOutfit ? currentOutfit.speeches : this.speeches;

      this.currentSpeech =
        speeches[Math.floor(Math.random() * speeches.length)];
      this.showBubble = true;

      setTimeout(() => {
        this.showBubble = false;
      }, 3000);
    },

    // 播放换装效果
    playOutfitChangeEffect() {
      // 简单的闪烁效果表示换装
      const mascotElement = this.$el?.querySelector(".mascot-image");
      if (mascotElement) {
        mascotElement.style.opacity = "0.3";
        setTimeout(() => {
          mascotElement.style.opacity = "1";
        }, 300);
      }

      // 显示换装提示
      this.currentSpeech = "我换新衣服啦~";
      this.showBubble = true;
      setTimeout(() => {
        this.showBubble = false;
      }, 2000);
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
      this.actions = this.actions.map((action) => ({
        ...action,
        image: outfit.images[action.name] || action.image,
      }));

      // 更新当前图片
      this.currentImage = outfit.images.idle;
      this.closeDressUp();

      this.showSpeech();
      this.currentSpeech = "新衣服很好看吧~";
    },

    // 长按事件（进入换装）
    onLongpress() {
      // this.openDressUp();
      uni.navigateTo({
        url: "/pages/dress-up/dress-up",
      });
    },
  },
};
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
  width: 130px;
  height: 156px;
  pointer-events: auto;
  transition: transform 0.3s ease;
}

.mascot-image {
  width: 100%;
  height: 100%;
  transition: opacity 0.3s ease-in-out;
}

.lottie-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
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
  content: "";
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
