<template>
    <view class="chat-section" :class="themeClass">
        <scroll-view 
            class="chat-history" 
            scroll-y="true" 
            :scroll-top="scrollTop" 
            scroll-with-animation="true"
            ref="scrollView"
        >
            <view v-for="(message, index) in displayedMessages" :key="index" 
                  :class="['message-container', message.role, { 'message-enter': messageAnimations[index] }]">
                <view :class="['message', message.role]">
                    <text class="message-text">{{ message.content }}</text>
                    <!-- 为AI消息添加光标闪烁效果 -->
                    <text v-if="message.role === 'assistant' && isTyping(message.content, index)" class="cursor">|</text>
                </view>
            </view>
            <view class="scroll-anchor" ref="scrollAnchor"></view>
        </scroll-view>
    </view>
</template>

<script>
export default {
    name: 'ChatMessages',
    props: {
        // 聊天消息列表
        messages: {
            type: Array,
            default: () => []
        },
        // 主题配色
        theme: {
            type: String,
            default: 'default', // default, emotion, interpersonal, tree-hole, student
            validator: value => ['default', 'emotion', 'interpersonal', 'tree-hole', 'student'].includes(value)
        }
    },
    data() {
        return {
            scrollTop: 0,
            displayedMessages: [],
            typingTimers: {}, // 存储每个消息的打字机定时器
            isAutoScroll: true,
            messageAnimations: {} // 消息动画状态
        }
    },
    computed: {
        // 根据主题返回样式类
        themeClass() {
            return `theme-${this.theme}`
        }
    },
    watch: {
        // 监听消息变化，自动滚动到底部
        messages: {
            handler(newMessages) {
                console.log('ChatMessages收到新消息:', newMessages)
                this.handleNewMessages(newMessages)
            },
            deep: true
        }
    },
    mounted() {
        // 初始化显示消息
        this.displayedMessages = JSON.parse(JSON.stringify(this.messages))
        // 为已存在的消息添加进入动画
        this.messages.forEach((_, index) => {
            this.$set(this.messageAnimations, index, false)
            setTimeout(() => {
                this.$set(this.messageAnimations, index, true)
            }, index * 100)
        })
    },
    methods: {
        handleNewMessages(newMessages) {
            // 确保 displayedMessages 至少与 messages 一样长
            while (this.displayedMessages.length < newMessages.length) {
                const newIndex = this.displayedMessages.length
                this.displayedMessages.push({
                    role: newMessages[newIndex].role,
                    content: ''
                })
                
                // 为新消息添加进入动画
                this.$set(this.messageAnimations, newIndex, false)
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.$set(this.messageAnimations, newIndex, true)
                    }, 50)
                })
            }
            
            // 处理每条消息
            newMessages.forEach((message, index) => {
                // 用户消息直接完整显示
                if (message.role === 'user') {
                    this.displayedMessages[index] = { ...message }
                    if (this.isAutoScroll) {
                        this.scrollToBottom()
                    }
                } 
                // AI消息使用打字机效果
                else if (message.role === 'assistant') {
                    // 如果已经有定时器在运行，先清除它
                    if (this.typingTimers[index]) {
                        clearInterval(this.typingTimers[index])
                        delete this.typingTimers[index]
                    }
                    
                    // 如果消息内容为空或者与已显示内容相同，直接显示
                    if (!message.content || this.displayedMessages[index].content === message.content) {
                        this.displayedMessages[index] = { ...message }
                        if (this.isAutoScroll) {
                            this.scrollToBottom()
                        }
                        return
                    }
                    
                    // 初始化显示内容为空
                    this.displayedMessages[index] = {
                        role: 'assistant',
                        content: ''
                    }
                    
                    // 通知父组件AI开始打字
                    this.$emit('ai-typing', true);
                    
                    // 启动打字机效果
                    this.typewriterEffect(index, message.content)
                }
            })
        },
        
        typewriterEffect(messageIndex, fullText) {
            let currentText = ''
            let charIndex = 0
            
            this.typingTimers[messageIndex] = setInterval(() => {
                if (charIndex < fullText.length) {
                    currentText += fullText.charAt(charIndex)
                    this.displayedMessages[messageIndex].content = currentText
                    charIndex++
                    if (this.isAutoScroll) {
                        this.scrollToBottom()
                    }
                } else {
                    // 完成打字，清除定时器
                    clearInterval(this.typingTimers[messageIndex])
                    delete this.typingTimers[messageIndex]
                    // 通知父组件AI结束打字
                    this.$emit('ai-typing', false);
                }
            }, 30) // 每30毫秒添加一个字符
        },
        
        isTyping(displayedContent, messageIndex) {
            // 检查指定消息是否仍在打字中
            const originalMessage = this.messages[messageIndex]
            return (
                originalMessage && 
                originalMessage.role === 'assistant' && 
                displayedContent !== originalMessage.content &&
                this.typingTimers[messageIndex] !== undefined
            )
        },
        
        scrollToBottom() {
            this.$nextTick(() => {
                // 使用一个足够大的值确保滚动到底部
                this.scrollTop = 999999
            })
        },
        
        // 提供给外部调用的强制滚动方法
        forceScrollToBottom() {
            this.isAutoScroll = true
            this.scrollToBottom()
        }
    },
    
    beforeDestroy() {
        // 组件销毁前清除所有定时器
        Object.values(this.typingTimers).forEach(timer => clearInterval(timer))
    }
}
</script>

<style scoped>
.chat-section {
    flex: 1;
    margin-bottom: 20rpx;
    background-color: #fff;
    border-radius: 15rpx;
    padding: 15rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.chat-history {
    flex: 1;
    height: 100%;
}

.message-container {
    margin-bottom: 15rpx;
    display: flex;
    opacity: 0;
    transform: translateY(30rpx);
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-container.message-enter {
    opacity: 1;
    transform: translateY(0);
}

.message-container.user {
    justify-content: flex-end;
}

.message-container.ai {
    justify-content: flex-start;
}

.message {
    border-radius: 18rpx;
    position: relative;
    word-wrap: break-word;
    word-break: break-word;
    display: inline-block;
    max-width: 80%;
    padding: 16rpx 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(10rpx);
    transition: transform 0.2s ease;
}

.message:active {
    transform: scale(0.98);
}

/* 默认主题 */
.message.user {
    background: linear-gradient(135deg, #007aff, #0056d3);
    color: white;
}

.message.ai {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    color: #333;
    border: 1rpx solid #dee2e6;
}

/* 情感对话主题 - 蓝色系 */
.theme-emotion .message.user {
    background: linear-gradient(135deg, #4fc3f7, #29b6f6);
    color: white;
}

.theme-emotion .message.ai {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    color: #1565c0;
    border: 1rpx solid #90caf9;
}

.theme-emotion .chat-section {
    background: linear-gradient(135deg, #f8fbff, #e8f4f8);
    border: 2rpx solid #e3f2fd;
}

/* 人际智慧主题 - 紫色系 */
.theme-interpersonal .message.user {
    background: linear-gradient(135deg, #ba68c8, #9c27b0);
    color: white;
}

.theme-interpersonal .message.ai {
    background: linear-gradient(135deg, #f3e5f5, #e1bee7);
    color: #6a1b9a;
    border: 1rpx solid #ce93d8;
}

.theme-interpersonal .chat-section {
    background: linear-gradient(135deg, #faf5ff, #f0e6ff);
    border: 2rpx solid #f3e5f5;
}

/* 心灵树洞主题 - 绿色系 */
.theme-tree-hole .message.user {
    background: linear-gradient(135deg, #66bb6a, #4caf50);
    color: white;
}

.theme-tree-hole .message.ai {
    background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
    color: #2e7d32;
    border: 1rpx solid #a5d6a7;
}

.theme-tree-hole .chat-section {
    background: linear-gradient(135deg, #f8fff8, #e8f8e8);
    border: 2rpx solid #e8f5e8;
}

/* 大学生专区主题 - 米黄色系 */
.theme-student .message.user {
    background: linear-gradient(135deg, #ffc107, #ff9800);
    color: white;
}

.theme-student .message.ai {
    background: linear-gradient(135deg, #fffbf0, #fff3e0);
    color: #e65100;
    border: 1rpx solid #ffcc02;
}

.theme-student .chat-section {
    background: linear-gradient(135deg, #fffef8, #faf7f0);
    border: 2rpx solid #fff3e0;
}

.message-text {
    font-size: 26rpx;
    line-height: 1.5;
    white-space: pre-wrap;
    display: block;
}

/* 光标闪烁动画 */
.cursor {
    animation: blink 1s infinite;
    font-size: 26rpx;
    line-height: 1.5;
    color: #007aff;
}

.theme-emotion .cursor {
    color: #29b6f6;
}

.theme-interpersonal .cursor {
    color: #9c27b0;
}

.theme-tree-hole .cursor {
    color: #4caf50;
}

.theme-student .cursor {
    color: #ff9800;
}

.scroll-anchor {
    height: 1rpx;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* 响应式设计 */
@media (max-width: 750rpx) {
    .message {
        max-width: 85%;
        padding: 14rpx 18rpx;
    }
    
    .message-text {
        font-size: 24rpx;
    }
}
</style>