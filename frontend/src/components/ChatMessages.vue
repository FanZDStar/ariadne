<!-- src/components/ChatMessages.vue -->
<template>
    <view class="chat-section">
        <scroll-view 
            class="chat-history" 
            scroll-y="true" 
            :scroll-top="scrollTop" 
            scroll-with-animation="true"
            ref="scrollView"
        >
            <view v-for="(message, index) in displayedMessages" :key="index" :class="['message-container', message.role]">
                <view :class="['message', message.role]">
                    <text class="message-text">{{ message.content }}</text>
                    <!-- 为AI消息添加光标闪烁效果 -->
                    <text v-if="message.role === 'ai' && isTyping(message.content, index)" class="cursor">|</text>
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
        }
    },
    data() {
        return {
            scrollTop: 0,
            displayedMessages: [],
            typingTimers: {}, // 存储每个消息的打字机定时器
            isAutoScroll: true
        }
    },
    watch: {
        // 监听消息变化，自动滚动到底部
        messages: {
            handler(newMessages) {
                this.handleNewMessages(newMessages)
            },
            deep: true
        }
    },
    mounted() {
        // 初始化显示消息
        this.displayedMessages = JSON.parse(JSON.stringify(this.messages))
    },
    methods: {
        handleNewMessages(newMessages) {
            // 确保 displayedMessages 至少与 messages 一样长
            while (this.displayedMessages.length < newMessages.length) {
                this.displayedMessages.push({
                    role: newMessages[this.displayedMessages.length].role,
                    content: ''
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
                else if (message.role === 'ai') {
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
                        role: 'ai',
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
                originalMessage.role === 'ai' && 
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
}

.message-container.user {
    justify-content: flex-end;
}

.message-container.ai {
    justify-content: flex-start;
}

.message {
    border-radius: 8rpx;
    position: relative;
    word-wrap: break-word;
    word-break: break-word;
    display: inline-block;
    max-width: 80%;
    padding: 15rpx;
}

.message.user {
    background-color: #007aff;
    color: white;
}

.message.ai {
    background-color: #f0f0f0;
    color: #333;
}

.message-text {
    font-size: 26rpx;
    line-height: 1.4;
    white-space: pre-wrap;
    display: block;
}

/* 光标闪烁动画 */
.cursor {
    animation: blink 1s infinite;
    font-size: 26rpx;
    line-height: 1.4;
}

.scroll-anchor {
    height: 1rpx;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
</style>