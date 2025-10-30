<template>
    <view class="multimodal-test">
        <!-- 标题区域 -->
        <view class="header">
            <text class="title">多模态AI测试</text>
            <text class="subtitle">文本对话 + 图片理解</text>
        </view>

        <!-- 功能选择 -->
        <view class="function-tabs">
            <view class="tab" :class="{ active: activeTab === 'text' }" @click="activeTab = 'text'">
                文本对话
            </view>
            <view class="tab" :class="{ active: activeTab === 'image' }" @click="activeTab = 'image'">
                图片理解
            </view>
        </view>

        <!-- 文本对话区域 -->
        <view v-if="activeTab === 'text'" class="text-chat-section">
            <view class="chat-history">
                <view v-for="(msg, index) in chatHistory" :key="index" class="message" :class="msg.role">
                    <text class="message-content">{{ msg.content }}</text>
                </view>
            </view>

            <view class="input-area">
                <input v-model="textInput" placeholder="输入你想说的话..." class="text-input" @confirm="sendTextMessage" />
                <button @click="sendTextMessage" :disabled="loading || !textInput.trim()" class="send-btn">
                    {{ loading ? '发送中...' : '发送' }}
                </button>
            </view>
        </view>

        <!-- 图片理解区域 -->
        <view v-if="activeTab === 'image'" class="image-chat-section">
            <!-- 图片预览 -->
            <view class="image-preview" v-if="selectedImage">
                <image :src="selectedImage" class="preview-img" mode="aspectFit" />
                <button @click="clearImage" class="clear-btn">清除图片</button>
            </view>

            <!-- 图片选择 -->
            <view class="image-actions" v-if="!selectedImage">
                <button @click="chooseImage" class="choose-btn">选择图片</button>
                <button @click="takePhoto" class="photo-btn">拍照</button>
            </view>

            <!-- 文字描述输入 -->
            <view class="description-area">
                <textarea v-model="imageDescription" placeholder="描述你想了解图片的什么内容..." class="description-input" />
                <button @click="analyzeImage" :disabled="loading || !selectedImage || !imageDescription.trim()"
                    class="analyze-btn">
                    {{ loading ? '分析中...' : '分析图片' }}
                </button>
            </view>

            <!-- 分析结果 -->
            <view class="analysis-result" v-if="analysisResult">
                <view class="result-title">AI分析结果：</view>
                <text class="result-content">{{ analysisResult }}</text>
            </view>
        </view>

        <!-- 模型状态 -->
        <view class="model-status">
            <text class="status-title">当前模型：</text>
            <text class="status-info">文本: {{ modelStatus.text_model || '未知' }}</text>
            <text class="status-info">视觉: {{ modelStatus.vision_model || '未知' }}</text>
        </view>

        <!-- 加载遮罩 -->
        <view v-if="loading" class="loading-mask">
            <view class="loading-content">
                <text class="loading-text">{{ loadingText }}</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            activeTab: 'text', // 'text' | 'image'

            // 文本对话
            textInput: '',
            chatHistory: [],

            // 图片理解
            selectedImage: '',
            selectedImageFile: null,
            imageDescription: '',
            analysisResult: '',

            // 状态
            loading: false,
            loadingText: '',
            modelStatus: {},

            // API配置
            apiBase: 'http://localhost:8000/multimodal'
        }
    },

    onLoad() {
        this.getModelStatus()
    },

    methods: {
        // ===== 文本对话功能 =====
        async sendTextMessage() {
            if (!this.textInput.trim() || this.loading) return

            const userMessage = {
                role: 'user',
                content: this.textInput.trim()
            }

            // 添加用户消息到历史
            this.chatHistory.push(userMessage)
            const currentInput = this.textInput
            this.textInput = ''

            this.loading = true
            this.loadingText = 'AI思考中...'

            try {
                const response = await uni.request({
                    url: `${this.apiBase}/chat/text`,
                    method: 'POST',
                    header: {
                        'Content-Type': 'application/json'
                    },
                    data: {
                        message: currentInput,
                        scene: 'general',
                        history: this.chatHistory.slice(-6) // 只发送最近6条消息
                    }
                })

                if (response.statusCode === 200 && response.data.content) {
                    // 添加AI回复到历史
                    this.chatHistory.push({
                        role: 'assistant',
                        content: response.data.content
                    })
                } else {
                    throw new Error('API响应异常')
                }

            } catch (error) {
                console.error('文本对话错误:', error)
                this.chatHistory.push({
                    role: 'assistant',
                    content: '抱歉，我遇到了一些问题，请稍后再试。'
                })

                uni.showToast({
                    title: '发送失败',
                    icon: 'none'
                })
            } finally {
                this.loading = false
                this.loadingText = ''
            }
        },

        // ===== 图片理解功能 =====
        chooseImage() {
            uni.chooseImage({
                count: 1,
                sizeType: ['compressed'],
                sourceType: ['album'],
                success: (res) => {
                    this.selectedImage = res.tempFilePaths[0]
                    this.selectedImageFile = res.tempFiles[0]
                    this.analysisResult = ''
                },
                fail: (error) => {
                    console.error('选择图片失败:', error)
                    uni.showToast({
                        title: '选择图片失败',
                        icon: 'none'
                    })
                }
            })
        },

        takePhoto() {
            uni.chooseImage({
                count: 1,
                sizeType: ['compressed'],
                sourceType: ['camera'],
                success: (res) => {
                    this.selectedImage = res.tempFilePaths[0]
                    this.selectedImageFile = res.tempFiles[0]
                    this.analysisResult = ''
                },
                fail: (error) => {
                    console.error('拍照失败:', error)
                    uni.showToast({
                        title: '拍照失败',
                        icon: 'none'
                    })
                }
            })
        },

        clearImage() {
            this.selectedImage = ''
            this.selectedImageFile = null
            this.analysisResult = ''
        },

        async analyzeImage() {
            if (!this.selectedImageFile || !this.imageDescription.trim() || this.loading) return

            this.loading = true
            this.loadingText = '图片分析中...'

            try {
                const response = await uni.uploadFile({
                    url: `${this.apiBase}/chat/image-upload`,
                    filePath: this.selectedImage,
                    name: 'image',
                    formData: {
                        text: this.imageDescription.trim(),
                        scene: 'image_analysis'
                    }
                })

                const result = JSON.parse(response.data)

                if (response.statusCode === 200 && result.content) {
                    this.analysisResult = result.content
                } else {
                    throw new Error('分析失败')
                }

            } catch (error) {
                console.error('图片分析错误:', error)
                this.analysisResult = '抱歉，图片分析失败，请稍后再试。'

                uni.showToast({
                    title: '分析失败',
                    icon: 'none'
                })
            } finally {
                this.loading = false
                this.loadingText = ''
            }
        },

        // ===== 工具方法 =====
        async getModelStatus() {
            try {
                const response = await uni.request({
                    url: `${this.apiBase}/models/status`,
                    method: 'GET'
                })

                if (response.statusCode === 200) {
                    this.modelStatus = response.data
                }
            } catch (error) {
                console.error('获取模型状态失败:', error)
            }
        }
    }
}
</script>

<style scoped>
.multimodal-test {
    padding: 20rpx;
    background-color: #f8f9fa;
    min-height: 100vh;
}

/* 标题区域 */
.header {
    text-align: center;
    margin-bottom: 30rpx;
}

.title {
    font-size: 48rpx;
    font-weight: bold;
    color: #2c3e50;
    display: block;
    margin-bottom: 10rpx;
}

.subtitle {
    font-size: 28rpx;
    color: #7f8c8d;
}

/* 功能选择标签 */
.function-tabs {
    display: flex;
    background-color: white;
    border-radius: 16rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.tab {
    flex: 1;
    text-align: center;
    padding: 24rpx;
    font-size: 32rpx;
    color: #7f8c8d;
    cursor: pointer;
}

.tab.active {
    color: #3498db;
    background-color: #ecf0f1;
    border-radius: 16rpx;
    font-weight: bold;
}

/* 文本对话区域 */
.text-chat-section {
    background-color: white;
    border-radius: 16rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.chat-history {
    max-height: 600rpx;
    overflow-y: auto;
    margin-bottom: 30rpx;
}

.message {
    margin-bottom: 20rpx;
    padding: 20rpx;
    border-radius: 12rpx;
    max-width: 80%;
}

.message.user {
    background-color: #3498db;
    color: white;
    margin-left: auto;
    text-align: right;
}

.message.assistant {
    background-color: #ecf0f1;
    color: #2c3e50;
}

.message-content {
    font-size: 30rpx;
    line-height: 1.5;
}

.input-area {
    display: flex;
    gap: 16rpx;
}

.text-input {
    flex: 1;
    padding: 20rpx;
    border: 2rpx solid #bdc3c7;
    border-radius: 12rpx;
    font-size: 30rpx;
}

.send-btn {
    padding: 20rpx 30rpx;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 12rpx;
    font-size: 30rpx;
}

.send-btn:disabled {
    background-color: #bdc3c7;
}

/* 图片理解区域 */
.image-chat-section {
    background-color: white;
    border-radius: 16rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.image-preview {
    text-align: center;
    margin-bottom: 30rpx;
}

.preview-img {
    width: 100%;
    max-height: 400rpx;
    border-radius: 12rpx;
    margin-bottom: 20rpx;
}

.clear-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 16rpx 30rpx;
    border-radius: 8rpx;
    font-size: 28rpx;
}

.image-actions {
    display: flex;
    gap: 20rpx;
    margin-bottom: 30rpx;
}

.choose-btn,
.photo-btn {
    flex: 1;
    padding: 24rpx;
    border: 2rpx solid #3498db;
    background-color: white;
    color: #3498db;
    border-radius: 12rpx;
    font-size: 30rpx;
}

.description-area {
    margin-bottom: 30rpx;
}

.description-input {
    width: 100%;
    height: 200rpx;
    padding: 20rpx;
    border: 2rpx solid #bdc3c7;
    border-radius: 12rpx;
    font-size: 30rpx;
    margin-bottom: 20rpx;
    box-sizing: border-box;
}

.analyze-btn {
    width: 100%;
    padding: 24rpx;
    background-color: #2ecc71;
    color: white;
    border: none;
    border-radius: 12rpx;
    font-size: 32rpx;
}

.analyze-btn:disabled {
    background-color: #bdc3c7;
}

.analysis-result {
    background-color: #f8f9fa;
    padding: 30rpx;
    border-radius: 12rpx;
    border-left: 8rpx solid #2ecc71;
}

.result-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 16rpx;
}

.result-content {
    font-size: 30rpx;
    color: #34495e;
    line-height: 1.6;
}

/* 模型状态 */
.model-status {
    background-color: white;
    border-radius: 16rpx;
    padding: 24rpx;
    margin-top: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.status-title {
    font-size: 28rpx;
    font-weight: bold;
    color: #2c3e50;
    display: block;
    margin-bottom: 12rpx;
}

.status-info {
    font-size: 26rpx;
    color: #7f8c8d;
    display: block;
    margin-bottom: 8rpx;
}

/* 加载遮罩 */
.loading-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loading-content {
    background-color: white;
    padding: 40rpx;
    border-radius: 16rpx;
    text-align: center;
}

.loading-text {
    font-size: 32rpx;
    color: #2c3e50;
}
</style>
