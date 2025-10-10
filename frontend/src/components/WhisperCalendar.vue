<template>
  <view class="calendar-overlay" @click="closeCalendar" v-if="visible">
    <view class="calendar-container" @click.stop>
      <view class="calendar-header">
        <view class="header-controls">
          <text class="nav-btn" @click="prevMonth">‹</text>
          <view class="date-selector">
            <text class="current-date" @click="toggleYearPicker">
              {{ currentYear }}年{{ currentMonth }}月
            </text>
          </view>
          <text class="nav-btn" @click="nextMonth">›</text>
        </view>
        <text class="close-btn" @click="closeCalendar">✕</text>
      </view>

      <!-- 年份选择器 -->
      <view v-if="showYearPicker" class="year-picker">
        <view 
          v-for="year in yearRange" 
          :key="year"
          :class="['year-item', { active: year === currentYear }]"
          @click="selectYear(year)"
        >
          {{ year }}
        </view>
      </view>

      <!-- 月历视图 -->
      <view v-else class="calendar-body">
        <view class="weekdays">
          <text class="weekday" v-for="day in weekDays" :key="day">{{ day }}</text>
        </view>
        <view class="days-grid">
          <view
            v-for="(day, index) in calendarDays"
            :key="index"
            :class="[
              'day-cell',
              { 'other-month': day.isOtherMonth },
              { 'has-whisper': day.hasWhisper },
              { 'selected': day.isSelected },
              { 'today': day.isToday }
            ]"
            @click="selectDate(day)"
          >
            <text class="day-number">{{ day.day }}</text>
            <view v-if="day.hasWhisper" class="whisper-dot"></view>
          </view>
        </view>
      </view>

      <view class="calendar-footer">
        <text class="reset-btn" @click="resetFilter">显示全部</text>
        <text class="hint-text">加粗日期有悄悄话</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'WhisperCalendar',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    whisperDates: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth() + 1,
      selectedDate: null,
      showYearPicker: false,
      weekDays: ['日', '一', '二', '三', '四', '五', '六']
    };
  },
  computed: {
    yearRange() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 5;
      const endYear = currentYear + 1;
      const years = [];
      for (let year = startYear; year <= endYear; year++) {
        years.push(year);
      }
      return years;
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
      const todayStr = this.formatDate(today);
      
      // 上个月的日期
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const day = daysInPrevMonth - i;
        const date = new Date(this.currentYear, this.currentMonth - 2, day);
        const dateStr = this.formatDate(date);
        days.push({
          day,
          date: dateStr,
          isOtherMonth: true,
          hasWhisper: this.hasWhisperOnDate(dateStr),
          isSelected: this.selectedDate === dateStr,
          isToday: dateStr === todayStr
        });
      }
      
      // 当前月的日期
      for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(this.currentYear, this.currentMonth - 1, day);
        const dateStr = this.formatDate(date);
        days.push({
          day,
          date: dateStr,
          isOtherMonth: false,
          hasWhisper: this.hasWhisperOnDate(dateStr),
          isSelected: this.selectedDate === dateStr,
          isToday: dateStr === todayStr
        });
      }
      
      // 下个月的日期（补充至42个格子，6行7列）
      const remainingDays = 42 - days.length;
      for (let day = 1; day <= remainingDays; day++) {
        const date = new Date(this.currentYear, this.currentMonth, day);
        const dateStr = this.formatDate(date);
        days.push({
          day,
          date: dateStr,
          isOtherMonth: true,
          hasWhisper: this.hasWhisperOnDate(dateStr),
          isSelected: this.selectedDate === dateStr,
          isToday: dateStr === todayStr
        });
      }
      
      return days;
    }
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    hasWhisperOnDate(dateStr) {
      return this.whisperDates.some(whisperDate => {
        const whisperDateStr = whisperDate.split('T')[0].split(' ')[0];
        return whisperDateStr === dateStr;
      });
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
      if (this.currentMonth === 12) {
        this.currentMonth = 1;
        this.currentYear++;
      } else {
        this.currentMonth++;
      }
    },
    toggleYearPicker() {
      this.showYearPicker = !this.showYearPicker;
    },
    selectYear(year) {
      this.currentYear = year;
      this.showYearPicker = false;
    },
    selectDate(day) {
      // 如果点击的是其他月份的日期
      if (day.isOtherMonth) {
        // 如果该日期有悄悄话，直接选择该日期并筛选
        if (day.hasWhisper) {
          this.selectedDate = day.date;
          this.$emit('date-selected', day.date);
          this.closeCalendar();
        } else {
          // 如果没有悄悄话，切换到对应月份查看
          const clickedDate = new Date(day.date);
          this.currentYear = clickedDate.getFullYear();
          this.currentMonth = clickedDate.getMonth() + 1;
        }
        return;
      }
      
      if (!day.hasWhisper) {
        uni.showToast({
          title: '该日期无悄悄话',
          icon: 'none',
          duration: 1500
        });
        return;
      }
      
      this.selectedDate = day.date;
      this.$emit('date-selected', day.date);
      this.closeCalendar();
    },
    resetFilter() {
      this.selectedDate = null;
      this.$emit('date-selected', null);
      this.closeCalendar();
    },
    closeCalendar() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.calendar-overlay {
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

.calendar-container {
  width: 90%;
  max-width: 680rpx;
  background: #ffffff;
  border-radius: 32rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.15);
}

.calendar-header {
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
  gap: 30rpx;
  flex: 1;
}

.nav-btn {
  font-size: 48rpx;
  color: #666;
  padding: 10rpx 20rpx;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-btn:active {
  color: #7c4dff;
}

.date-selector {
  flex: 1;
  text-align: center;
}

.current-date {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.close-btn {
  font-size: 40rpx;
  color: #999;
  padding: 10rpx;
  cursor: pointer;
}

.year-picker {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
  max-height: 500rpx;
  overflow-y: auto;
}

.year-item {
  padding: 20rpx;
  text-align: center;
  border-radius: 12rpx;
  background: #f5f5f5;
  font-size: 28rpx;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.year-item.active {
  background: #7c4dff;
  color: #ffffff;
  font-weight: 600;
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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12rpx;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.day-cell.other-month .day-number {
  color: #d0d0d0;
}

.day-cell.has-whisper .day-number {
  font-weight: 700;
  color: #333;
}

.day-cell.selected {
  background: #7c4dff;
}

.day-cell.selected .day-number {
  color: #ffffff !important;
}

.day-cell.today {
  border: 2px solid #7c4dff;
}

.day-cell:active {
  background: #f0f0f0;
}

.day-cell.selected:active {
  background: #6c3de8;
}

.day-number {
  font-size: 28rpx;
  color: #666;
}

.whisper-dot {
  width: 8rpx;
  height: 8rpx;
  background: #7c4dff;
  border-radius: 50%;
  position: absolute;
  bottom: 8rpx;
}

.day-cell.selected .whisper-dot {
  background: #ffffff;
}

.calendar-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 30rpx;
  border-top: 1px solid #f0f0f0;
}

.reset-btn {
  padding: 16rpx 40rpx;
  background: #7c4dff;
  color: #ffffff;
  border-radius: 40rpx;
  font-size: 28rpx;
  cursor: pointer;
  transition: background 0.3s;
}

.reset-btn:active {
  background: #6c3de8;
}

.hint-text {
  font-size: 24rpx;
  color: #999;
}
</style>
