/**
 * 前端隐私数据处理工具
 * 处理敏感数据的显示和提交
 */

export class PrivacyManager {

    /**
     * 检查数据是否需要特殊处理
     * @param {Object} data - 数据对象
     * @param {string} type - 数据类型 (diary, whisper, chat)
     * @returns {boolean}
     */
    static needsPrivacyProtection(data, type) {
        switch (type) {
            case 'diary':
                return data.is_private === true;
            case 'whisper':
            case 'comment':
                return data.is_anonymous === true;
            case 'chat':
                return true; // 聊天记录始终需要保护
            default:
                return false;
        }
    }

    /**
     * 处理敏感数据的显示
     * @param {Object} data - 原始数据
     * @param {string} type - 数据类型
     * @returns {Object} 处理后的数据
     */
    static processForDisplay(data, type) {
        // 前端不需要做加密，只是标记敏感数据
        if (this.needsPrivacyProtection(data, type)) {
            return {
                ...data,
                _isEncrypted: true,
                _privacyType: type
            };
        }
        return data;
    }

    /**
     * 处理提交前的数据
     * @param {Object} data - 要提交的数据
     * @param {string} type - 数据类型
     * @returns {Object} 处理后的数据
     */
    static processForSubmit(data, type) {
        // 前端只需要正确设置隐私标记，加密由后端处理
        const processedData = { ...data };

        switch (type) {
            case 'diary':
                // 确保私密日记标记正确
                if (processedData.is_private === undefined) {
                    processedData.is_private = true; // 默认私密
                }
                break;
            case 'whisper':
                // 确保匿名悄悄话标记正确
                if (processedData.is_anonymous === undefined) {
                    processedData.is_anonymous = true; // 默认匿名
                }
                break;
            case 'comment':
                // 确保匿名评论标记正确
                if (processedData.is_anonymous === undefined) {
                    processedData.is_anonymous = true; // 默认匿名
                }
                break;
        }

        return processedData;
    }

    /**
     * 获取隐私提示文本
     * @param {string} type - 数据类型
     * @param {boolean} isPrivate - 是否私密
     * @returns {string}
     */
    static getPrivacyHint(type, isPrivate) {
        if (!isPrivate) return '';

        switch (type) {
            case 'diary':
                return '🔒 此日记内容已加密保护';
            case 'whisper':
                return '🔒 匿名悄悄话内容已加密保护';
            case 'comment':
                return '🔒 匿名评论内容已加密保护';
            case 'chat':
                return '🔒 聊天记录已加密保护';
            default:
                return '🔒 内容已加密保护';
        }
    }

    /**
     * 生成隐私设置选项
     * @param {string} type - 数据类型
     * @returns {Array} 选项数组
     */
    static getPrivacyOptions(type) {
        switch (type) {
            case 'diary':
                return [
                    { value: true, label: '私密日记', description: '只有自己可见，内容加密存储' },
                    { value: false, label: '公开日记', description: '其他用户可能看到，内容明文存储' }
                ];
            case 'whisper':
                return [
                    { value: true, label: '匿名发布', description: '隐藏身份，内容加密存储' },
                    { value: false, label: '实名发布', description: '显示昵称，内容明文存储' }
                ];
            case 'comment':
                return [
                    { value: true, label: '匿名评论', description: '隐藏身份，内容加密存储' },
                    { value: false, label: '实名评论', description: '显示昵称，内容明文存储' }
                ];
            default:
                return [];
        }
    }

    /**
     * 验证敏感内容
     * @param {string} content - 内容
     * @param {string} type - 类型
     * @returns {Object} 验证结果
     */
    static validateSensitiveContent(content, type) {
        const result = {
            isValid: true,
            warnings: [],
            errors: []
        };

        // 检查内容长度
        if (!content || content.trim().length === 0) {
            result.isValid = false;
            result.errors.push('内容不能为空');
            return result;
        }

        // 检查敏感信息（简单检查）
        const sensitivePatterns = [
            /\d{11}/, // 手机号
            /\d{15,18}/, // 身份证号
            /[\w\.-]+@[\w\.-]+\.\w+/, // 邮箱
        ];

        sensitivePatterns.forEach(pattern => {
            if (pattern.test(content)) {
                result.warnings.push('检测到可能的敏感信息，建议设为私密');
            }
        });

        return result;
    }
}

// 导出单例
export const privacyManager = new PrivacyManager();
