<template>
    <view v-if="visible" class="back-to-top" :style="buttonStyle" @click="scrollToTop">
        <image src="../static/backToTop.png" class="back-to-top-icon"></image>
    </view>
</template>

<script>
export default {
    name: 'BackToTop',
    props: {
        threshold: {
            type: Number,
            default: 300
        },
        bottom: {
            type: Number,
            default: 80
        },
        right: {
            type: Number,
            default: 30
        },
        duration: {
            type: Number,
            default: 50
        }
    },
    data() {
        return {
            visible: false
        }
    },
    computed: {
        buttonStyle() {
            return {
                bottom: this.bottom + 'rpx',
                right: this.right + 'rpx'
            }
        }
    },
    mounted() {
        this.$emit('start-scroll-listener')
    },
    beforeDestroy() {
        this.$emit('remove-scroll-listener')
    },
    methods: {
        updateVisibility(scrollTop) {
            this.visible = scrollTop > this.threshold
        },
        scrollToTop() {
            uni.pageScrollTo({
                scrollTop: 0,
                duration: this.duration,
                success: () => {
                    this.$emit('scroll-to-top-success')
                }
            })
        }
    }
}
</script>

<style scoped>
.back-to-top {
    position: fixed;
    width: 100rpx;
    height: 100rpx;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    transition: opacity 0.3s ease;
}

.back-to-top-icon {
    width: 60rpx;
    height: 60rpx;
}
</style>
