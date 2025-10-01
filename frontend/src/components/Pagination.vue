<template>
    <view class="pagination-container" v-if="totalPages > 1">
        <view class="pagination">
            <!-- 上一页按钮 -->
            <view class="page-btn prev-btn" :class="{ disabled: currentPage <= 1 }" @click="goToPrevPage">
                <text class="page-text">上一页</text>
            </view>

            <!-- 页码显示 -->
            <view class="page-info">
                <text class="page-current">{{ currentPage }}</text>
                <text class="page-separator">/</text>
                <text class="page-total">{{ totalPages }}</text>
            </view>

            <!-- 下一页按钮 -->
            <view class="page-btn next-btn" :class="{ disabled: currentPage >= totalPages }" @click="goToNextPage">
                <text class="page-text">下一页</text>
            </view>
        </view>

        <!-- 页面跳转 -->
        <view class="page-jump" v-if="totalPages > 3">
            <text class="jump-text">跳转到</text>
            <input class="jump-input" :class="{ 'invalid': jumpPage && !isJumpPageValid }" type="number"
                v-model.number="jumpPage" @confirm="jumpToPage" @input="onInputChange"
                :placeholder="'1-' + totalPages" />
            <text class="jump-text">页</text>
            <view class="jump-btn" :class="{ disabled: !jumpPage || !isJumpPageValid }" @click="jumpToPage">
                <text class="jump-btn-text">跳转</text>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'Pagination',
    props: {
        currentPage: {
            type: Number,
            default: 1
        },
        pageSize: {
            type: Number,
            default: 8
        },
        total: {
            type: Number,
            default: 0
        }
    },
    data() {
        return {
            jumpPage: ''
        }
    },
    computed: {
        totalPages() {
            return Math.ceil(this.total / this.pageSize)
        },
        isJumpPageValid() {
            if (!this.jumpPage || this.jumpPage === '') return true // 空值时不显示错误样式
            const page = parseInt(this.jumpPage)
            return !isNaN(page) && page >= 1 && page <= this.totalPages && page !== this.currentPage
        }
    },
    methods: {
        goToPrevPage() {
            if (this.currentPage > 1) {
                this.$emit('page-change', this.currentPage - 1)
            }
        },
        goToNextPage() {
            if (this.currentPage < this.totalPages) {
                this.$emit('page-change', this.currentPage + 1)
            }
        },
        jumpToPage() {
            // 如果按钮处于禁用状态，直接返回
            if (!this.jumpPage || !this.isJumpPageValid) {
                return
            }

            // 如果输入框为空，提示用户
            if (String(this.jumpPage).trim() === '') {
                uni.showToast({
                    title: '请输入页码',
                    icon: 'none'
                })
                return
            }

            const page = parseInt(this.jumpPage)

            // 检查页码是否有效（包括NaN、小于1、大于总页数的情况）
            if (isNaN(page) || page < 1 || page > this.totalPages) {
                uni.showToast({
                    title: `请输入1-${this.totalPages}之间的页码`,
                    icon: 'none'
                })
                // 不清空输入框，让用户看到自己输入了什么
                return
            }

            // 检查是否与当前页相同
            if (page === this.currentPage) {
                uni.showToast({
                    title: '已经在当前页了',
                    icon: 'none'
                })
                this.jumpPage = ''
                return
            }

            // 执行跳转
            this.$emit('page-change', page)
            this.jumpPage = ''

            // 显示成功提示
            uni.showToast({
                title: `已跳转到第${page}页`,
                icon: 'success',
                duration: 1500
            })
        },
        onInputChange(e) {
            // 实时验证输入，但不清空输入框，让用户看到自己输入的内容
            // 在跳转时再进行完整的验证和提示
            this.jumpPage = e.detail.value
        }
    }
}
</script>

<style scoped>
.pagination-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40rpx 30rpx;
    background-color: #f5f5f5;
}

.pagination {
    display: flex;
    align-items: center;
    gap: 20rpx;
    background-color: white;
    padding: 20rpx 30rpx;
    border-radius: 50rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.page-btn {
    padding: 16rpx 32rpx;
    border-radius: 25rpx;
    background: linear-gradient(135deg, #ffafcc, #ffc8dd);
    transition: all 0.3s ease;
    min-width: 120rpx;
    text-align: center;
}

.page-btn:active {
    transform: scale(0.95);
}

.page-btn.disabled {
    background: #e0e0e0;
    opacity: 0.5;
}

.page-text {
    font-size: 28rpx;
    color: white;
    font-weight: 500;
}

.page-btn.disabled .page-text {
    color: #999;
}

.page-info {
    display: flex;
    align-items: center;
    gap: 8rpx;
    padding: 0 20rpx;
}

.page-current {
    font-size: 32rpx;
    font-weight: bold;
    color: #ffafcc;
}

.page-separator {
    font-size: 28rpx;
    color: #999;
}

.page-total {
    font-size: 28rpx;
    color: #666;
}

.page-jump {
    display: flex;
    align-items: center;
    gap: 15rpx;
    margin-top: 30rpx;
    background-color: white;
    padding: 20rpx 30rpx;
    border-radius: 50rpx;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.jump-text {
    font-size: 26rpx;
    color: #666;
}

.jump-input {
    width: 120rpx;
    height: 60rpx;
    text-align: center;
    border: 2rpx solid #ddd;
    border-radius: 15rpx;
    font-size: 26rpx;
    background-color: #f9f9f9;
}

.jump-input:focus {
    border-color: #ffafcc;
    background-color: white;
}

.jump-input.invalid {
    border-color: #ff6b6b;
    background-color: #fff5f5;
    color: #ff6b6b;
}

.jump-input.invalid:focus {
    border-color: #ff6b6b;
    background-color: #fff5f5;
}

.jump-btn {
    background: linear-gradient(135deg, #ffafcc, #ffc8dd);
    padding: 15rpx 25rpx;
    border-radius: 15rpx;
    transition: all 0.3s ease;
    box-shadow: 0 2rpx 6rpx rgba(255, 175, 204, 0.3);
}

.jump-btn:active {
    transform: scale(0.95);
    box-shadow: 0 1rpx 3rpx rgba(255, 175, 204, 0.5);
}

.jump-btn.disabled {
    background: #e0e0e0;
    opacity: 0.6;
    box-shadow: none;
}

.jump-btn.disabled:active {
    transform: none;
}

.jump-btn-text {
    font-size: 24rpx;
    color: white;
    font-weight: 500;
}

.jump-btn.disabled .jump-btn-text {
    color: #999;
}
</style>
