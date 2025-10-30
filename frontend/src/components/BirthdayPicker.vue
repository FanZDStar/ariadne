<template>
    <view class="picker-overlay" @click="closeCalendar" v-if="visible">
        <view class="picker-container" @click.stop>
            <!-- 头部 -->
            <view class="picker-header">
                <view class="header-controls">
                    <text class="nav-btn" @click="prevMonth">‹</text>
                    <view class="date-display">
                        <text class="year-text" @click="toggleYearPicker">
                            {{ currentYear }}年
                        </text>
                        <text class="month-text" @click="toggleMonthPicker">
                            {{ String(currentMonth).padStart(2, '0') }}月
                        </text>
                    </view>
                    <text class="nav-btn" @click="nextMonth">›</text>
                </view>
                <text class="close-btn" @click="closeCalendar">✕</text>
            </view>

            <!-- 年份选择器 -->
            <view v-if="showYearPicker" class="year-picker">
                <view class="picker-title">选择年份</view>
                <view class="picker-items">
                    <view v-for="year in yearRange" :key="year"
                        :class="['picker-item', { active: year === currentYear }]" @click="selectYear(year)">
                        {{ year }}
                    </view>
                </view>
            </view>

            <!-- 月份选择器 -->
            <view v-else-if="showMonthPicker" class="month-picker">
                <view class="picker-title">选择月份</view>
                <view class="picker-items">
                    <view v-for="month in 12" :key="month" :class="['picker-item', { active: month === currentMonth }]"
                        @click="selectMonth(month)">
                        {{ String(month).padStart(2, '0') }}
                    </view>
                </view>
            </view>

            <!-- 日期选择器 -->
            <view v-else class="calendar-body">
                <view class="weekdays">
                    <text class="weekday" v-for="day in weekDays" :key="day">{{ day }}</text>
                </view>
                <view class="days-grid">
                    <view v-for="(day, index) in calendarDays" :key="index" :class="[
                        'day-cell',
                        { 'other-month': day.isOtherMonth },
                        { 'selected': day.isSelected },
                        { 'today': day.isToday },
                        { 'disabled': day.isDisabled }
                    ]" @click="selectDate(day)">
                        <text class="day-number">{{ day.day }}</text>
                    </view>
                </view>
            </view>

            <!-- 底部按钮 -->
            <view class="picker-footer" v-if="!showYearPicker && !showMonthPicker">
                <text class="hint-text">
                    已选择: {{ selectedDateDisplay }}
                </text>
                <view class="footer-buttons">
                    <text class="btn-cancel" @click="cancel">取消</text>
                    <text class="btn-confirm" @click="confirm">确定</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    name: 'BirthdayPicker',
    props: {
        visible: {
            type: Boolean,
            default: false
        },
        modelValue: {
            type: String,
            default: ''
        }
    },
    data() {
        const today = new Date();
        return {
            currentYear: today.getFullYear(),
            currentMonth: today.getMonth() + 1,
            currentDay: today.getDate(),
            showYearPicker: false,
            showMonthPicker: false,
            weekDays: ['日', '一', '二', '三', '四', '五', '六'],
            tempSelectedDate: this.modelValue || ''
        };
    },
    computed: {
        yearRange() {
            const today = new Date();
            const currentYear = today.getFullYear();
            const startYear = currentYear - 100;
            const endYear = currentYear;
            const years = [];
            for (let year = startYear; year <= endYear; year++) {
                years.push(year);
            }
            return years.reverse();
        },
        calendarDays() {
            const days = [];
            const firstDay = new Date(this.currentYear, this.currentMonth - 1, 1);
            const lastDay = new Date(this.currentYear, this.currentMonth, 0);
            const prevLastDay = new Date(this.currentYear, this.currentMonth - 1, 0);

            const firstDayOfWeek = firstDay.getDay();
            const daysInMonth = lastDay.getDate();
            const daysInPrevMonth = prevLastDay.getDate();

            const today = new Date();
            today.setHours(0, 0, 0, 0); // 重置时间为00:00:00
            const todayStr = this.formatDate(today);

            // 上个月的日期
            for (let i = firstDayOfWeek - 1; i >= 0; i--) {
                const day = daysInPrevMonth - i;
                const date = new Date(this.currentYear, this.currentMonth - 2, day);
                const dateStr = this.formatDate(date);
                const isDisabled = new Date(dateStr) > today; // 超过今天则禁用
                days.push({
                    day,
                    date: dateStr,
                    isOtherMonth: true,
                    isSelected: this.tempSelectedDate === dateStr,
                    isToday: dateStr === todayStr,
                    isDisabled
                });
            }

            // 当前月的日期
            for (let day = 1; day <= daysInMonth; day++) {
                const date = new Date(this.currentYear, this.currentMonth - 1, day);
                const dateStr = this.formatDate(date);
                const isDisabled = new Date(dateStr) > today; // 超过今天则禁用
                days.push({
                    day,
                    date: dateStr,
                    isOtherMonth: false,
                    isSelected: this.tempSelectedDate === dateStr,
                    isToday: dateStr === todayStr,
                    isDisabled
                });
            }

            // 下个月的日期（补充至42个格子）
            const remainingDays = 42 - days.length;
            for (let day = 1; day <= remainingDays; day++) {
                const date = new Date(this.currentYear, this.currentMonth, day);
                const dateStr = this.formatDate(date);
                const isDisabled = new Date(dateStr) > today; // 超过今天则禁用
                days.push({
                    day,
                    date: dateStr,
                    isOtherMonth: true,
                    isSelected: this.tempSelectedDate === dateStr,
                    isToday: dateStr === todayStr,
                    isDisabled
                });
            }

            return days;
        },
        selectedDateDisplay() {
            if (!this.tempSelectedDate) {
                return '未选择';
            }
            const date = new Date(this.tempSelectedDate);
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            });
        }
    },
    watch: {
        modelValue(newVal) {
            if (newVal) {
                this.tempSelectedDate = newVal;
                const date = new Date(newVal);
                this.currentYear = date.getFullYear();
                this.currentMonth = date.getMonth() + 1;
                this.currentDay = date.getDate();
            }
        },
        visible(newVal) {
            if (newVal && this.modelValue) {
                const date = new Date(this.modelValue);
                this.currentYear = date.getFullYear();
                this.currentMonth = date.getMonth() + 1;
                this.currentDay = date.getDate();
                this.tempSelectedDate = this.modelValue;
            }
        }
    },
    methods: {
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        prevMonth() {
            if (this.currentMonth === 1) {
                this.currentMonth = 12;
                this.currentYear--;
            } else {
                this.currentMonth--;
            }
        },
        nextMonth() {
            const today = new Date();
            const nextMonthDate = new Date(this.currentYear, this.currentMonth, 1);

            // 不允许导航到未来的月份
            if (nextMonthDate >= today) {
                return;
            }

            if (this.currentMonth === 12) {
                this.currentMonth = 1;
                this.currentYear++;
            } else {
                this.currentMonth++;
            }
        },
        toggleYearPicker() {
            this.showYearPicker = !this.showYearPicker;
            this.showMonthPicker = false;
        },
        toggleMonthPicker() {
            this.showMonthPicker = !this.showMonthPicker;
            this.showYearPicker = false;
        },
        selectYear(year) {
            // 不允许选择未来的年份
            const today = new Date();
            if (year > today.getFullYear()) {
                return;
            }

            this.currentYear = year;
            this.showYearPicker = false;
        },
        selectMonth(month) {
            const today = new Date();

            // 如果是当前年份，不允许选择未来的月份
            if (this.currentYear === today.getFullYear() && month > today.getMonth() + 1) {
                return;
            }

            this.currentMonth = month;
            this.showMonthPicker = false;
        },
        selectDate(day) {
            // 如果日期被禁用，不允许选择
            if (day.isDisabled) {
                return;
            }

            if (day.isOtherMonth) {
                const clickedDate = new Date(day.date);
                this.currentYear = clickedDate.getFullYear();
                this.currentMonth = clickedDate.getMonth() + 1;
                return;
            }

            this.tempSelectedDate = day.date;
            this.currentDay = day.day;
        },
        cancel() {
            this.tempSelectedDate = this.modelValue;
            this.closeCalendar();
        },
        confirm() {
            this.$emit('update:modelValue', this.tempSelectedDate);
            this.$emit('selected', this.tempSelectedDate);
            this.closeCalendar();
        },
        closeCalendar() {
            this.$emit('close');
        }
    }
};
</script>

<style scoped>
.picker-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.picker-container {
    width: 90%;
    max-width: 680rpx;
    background: #ffffff;
    border-radius: 32rpx;
    padding: 40rpx;
    box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.15);
}

.picker-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40rpx;
    padding-bottom: 30rpx;
    border-bottom: 1px solid #f0f0f0;
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 20rpx;
    flex: 1;
}

.nav-btn {
    font-size: 48rpx;
    color: #666;
    padding: 10rpx 15rpx;
    cursor: pointer;
    transition: color 0.3s;
}

.nav-btn:active {
    color: #667eea;
}

.date-display {
    flex: 1;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10rpx;
}

.year-text,
.month-text {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    padding: 8rpx 12rpx;
    border-radius: 8rpx;
    transition: background 0.3s;
}

.year-text:active,
.month-text:active {
    background: #f0f0f0;
}

.close-btn {
    font-size: 40rpx;
    color: #999;
    padding: 10rpx;
    cursor: pointer;
}

.picker-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 20rpx;
    text-align: center;
}

.year-picker,
.month-picker {
    margin-bottom: 30rpx;
}

.picker-items {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15rpx;
    max-height: 400rpx;
    overflow-y: auto;
}

.picker-item {
    padding: 20rpx;
    text-align: center;
    border-radius: 12rpx;
    background: #f5f5f5;
    font-size: 28rpx;
    color: #666;
    cursor: pointer;
    transition: all 0.3s;
}

.picker-item.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    font-weight: 600;
}

.picker-item:active {
    opacity: 0.8;
}

.calendar-body {
    margin-bottom: 30rpx;
}

.weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    margin-bottom: 20rpx;
}

.weekday {
    text-align: center;
    font-size: 26rpx;
    color: #999;
    padding: 20rpx 0;
    font-weight: 500;
}

.days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8rpx;
}

.day-cell {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12rpx;
    cursor: pointer;
    position: relative;
    transition: all 0.2s;
}

.day-cell.disabled {
    color: #d0d0d0;
    cursor: not-allowed;
    background-color: transparent;
    opacity: 0.5;
}

.day-cell.other-month .day-number {
    color: #d0d0d0;
}

.day-cell.selected {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.day-cell.selected .day-number {
    color: #ffffff;
    font-weight: 700;
}

.day-cell.today {
    border: 2px solid #667eea;
}

.day-cell:active {
    background: #f0f0f0;
}

.day-cell.selected:active {
    opacity: 0.9;
}

.day-number {
    font-size: 28rpx;
    color: #666;
}

.picker-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30rpx;
    border-top: 1px solid #f0f0f0;
}

.hint-text {
    font-size: 26rpx;
    color: #667eea;
    font-weight: 600;
}

.footer-buttons {
    display: flex;
    gap: 20rpx;
}

.btn-cancel,
.btn-confirm {
    padding: 12rpx 30rpx;
    border-radius: 20rpx;
    font-size: 26rpx;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-cancel {
    background: #f0f0f0;
    color: #666;
}

.btn-cancel:active {
    background: #e0e0e0;
}

.btn-confirm {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
}

.btn-confirm:active {
    opacity: 0.9;
}
</style>
