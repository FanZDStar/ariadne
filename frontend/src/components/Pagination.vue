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
            <input class="jump-input" type="number" v-model.number="jumpPage" @confirm="jumpToPage"
                :placeholder="'1-' + totalPages" />
            <text class="jump-text">页</text>
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
            const page = parseInt(this.jumpPage)
            if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
                this.$emit('page-change', page)
                this.jumpPage = ''
            } else {
                uni.showToast({
                    title: '页码无效',
                    icon: 'none'
                })
            }
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
</style>
