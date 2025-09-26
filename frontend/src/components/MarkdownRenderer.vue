<template>
  <view class="markdown-content" v-html="renderedHtml"></view>
</template>

<script>
import MarkdownIt from "markdown-it";

export default {
  name: "MarkdownRenderer",
  props: {
    content: {
      type: String,
      default: "",
    },
  },

  data() {
    return {
      md: null,
    };
  },

  computed: {
    renderedHtml() {
      if (!this.content || !this.md) return "";
      return this.md.render(this.content);
    },
  },

  mounted() {
    // 初始化 markdown-it 实例
    this.md = new MarkdownIt({
      html: true, // 允许HTML标签
      xhtmlOut: true, // 输出XHTML兼容的标签
      breaks: true, // 将换行符转换为 <br>
      linkify: true, // 自动识别链接
      typographer: true, // 启用一些语言中性的替换和引号美化
    });
  },
};
</script>

<style scoped>
.markdown-content {
  line-height: 1.6;
}

/* 标题样式 */
.markdown-content :deep(h1) {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin: 20rpx 0 15rpx 0;
}

.markdown-content :deep(h2) {
  font-size: 30rpx;
  font-weight: bold;
  color: #444;
  margin: 18rpx 0 12rpx 0;
}

.markdown-content :deep(h3) {
  font-size: 28rpx;
  font-weight: bold;
  color: #555;
  margin: 15rpx 0 10rpx 0;
}

.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  font-size: 26rpx;
  font-weight: bold;
  color: #666;
  margin: 12rpx 0 8rpx 0;
}

/* 段落样式 */
.markdown-content :deep(p) {
  font-size: 26rpx;
  color: #555;
  margin-bottom: 15rpx;
  line-height: 1.6;
}

/* 列表样式 */
.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 15rpx 0;
  padding-left: 40rpx;
}

.markdown-content :deep(li) {
  font-size: 26rpx;
  color: #555;
  margin-bottom: 8rpx;
  line-height: 1.5;
}

.markdown-content :deep(ul li) {
  list-style-type: disc;
}

.markdown-content :deep(ol li) {
  list-style-type: decimal;
}

/* 分隔线 */
.markdown-content :deep(hr) {
  border: none;
  height: 2rpx;
  background: linear-gradient(90deg, transparent, #ddd, transparent);
  margin: 20rpx 0;
}

/* 强调样式 */
.markdown-content :deep(em) {
  font-style: italic;
  color: #666;
}

.markdown-content :deep(strong) {
  font-weight: bold;
  color: #333;
}

/* 代码样式 */
.markdown-content :deep(code) {
  background: #f5f5f5;
  padding: 4rpx 8rpx;
  border-radius: 6rpx;
  font-family: "Courier New", monospace;
  font-size: 24rpx;
  color: #d63384;
}

.markdown-content :deep(pre) {
  background: #f5f5f5;
  padding: 20rpx;
  border-radius: 10rpx;
  overflow-x: auto;
  margin: 15rpx 0;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  color: #333;
}

/* 引用样式 */
.markdown-content :deep(blockquote) {
  border-left: 6rpx solid #667eea;
  padding-left: 20rpx;
  margin: 15rpx 0;
  background: #f8f9fa;
  padding: 20rpx;
  border-radius: 0 10rpx 10rpx 0;
}

.markdown-content :deep(blockquote p) {
  color: #666;
  font-style: italic;
  margin-bottom: 0;
}

/* 链接样式 */
.markdown-content :deep(a) {
  color: #667eea;
  text-decoration: underline;
}

/* 表格样式 */
.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 15rpx 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  padding: 12rpx;
  text-align: left;
  border: 1rpx solid #ddd;
  font-size: 24rpx;
}

.markdown-content :deep(th) {
  background: #f8f9fa;
  font-weight: bold;
  color: #333;
}
</style>
