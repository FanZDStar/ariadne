/**
 * 看板娘显示配置
 * 定义哪些页面需要显示看板娘
 */

// 需要显示看板娘的页面路由前缀
export const MASCOT_ENABLED_PAGES = [
    // 心灵树洞相关页面
    '/pages/tree-hole/tree-hole',
    '/pages/tree-hole/write-whisper',
    '/pages/tree-hole/edit-whisper',
    '/pages/tree-hole/listen-whisper',
    '/pages/tree-hole/whisper-detail',
    '/pages/tree-hole/whisper-chat',
    '/pages/tree-hole/my-whispers',

    // 人际智慧相关页面
    '/pages/interpersonal-wisdom/interpersonal-wisdom',
    '/pages/interpersonal-wisdom/category-detail',
    '/pages/interpersonal-wisdom/skill-detail',
    '/pages/interpersonal-wisdom/skill-practice',
    '/pages/interpersonal-wisdom/skill-favorites',
    '/pages/interpersonal-wisdom/interactive-practice',
    '/pages/interpersonal-wisdom/practice-detail',
    '/pages/interpersonal-wisdom/practice-history',
    '/pages/interpersonal-wisdom/protection-drill',
    '/pages/interpersonal-wisdom/protection-drill-report-detail',
    '/pages/interpersonal-wisdom/protection-drill-reports',
    '/pages/interpersonal-wisdom/scenario-simulation',
    '/pages/interpersonal-wisdom/assessment-reports',
    '/pages/interpersonal-wisdom/report-detail',
    '/pages/interpersonal-wisdom/personalized-advice',
    '/pages/interpersonal-wisdom/emergency-resources',
    '/pages/interpersonal-wisdom/risk-assessment',

    // 首页（已有）
    '/pages/home/home',
];

/**
 * 检查当前页面是否应该显示看板娘
 * @param {string} currentPagePath - 当前页面路径
 * @returns {boolean} - 是否显示看板娘
 */
export function shouldShowMascot(currentPagePath) {
    return MASCOT_ENABLED_PAGES.some(page => currentPagePath.includes(page));
}

/**
 * 获取所有启用看板娘的页面
 * @returns {array} - 页面路由列表
 */
export function getMascotEnabledPages() {
    return MASCOT_ENABLED_PAGES;
}
