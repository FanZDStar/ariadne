# 看板娘换装页面资源说明

## 目录结构
```
static/
├── mascot/          # 看板娘完整形象图片
│   ├── default-full.png    # 默认装完整形象
│   ├── summer-full.png     # 夏日清新完整形象
│   ├── school-full.png     # 校园风完整形象
│   ├── sport-full.png      # 运动装完整形象
│   ├── formal-full.png     # 正装完整形象
│   ├── casual-full.png     # 休闲装完整形象
│   ├── evening-full.png    # 晚礼服完整形象
│   └── cute-full.png       # 可爱风完整形象
└── outfits/         # 服装预览小图
    ├── default-preview.png  # 默认装预览
    ├── summer-preview.png   # 夏日清新预览
    ├── school-preview.png   # 校园风预览
    ├── sport-preview.png    # 运动装预览
    ├── formal-preview.png   # 正装预览
    ├── casual-preview.png   # 休闲装预览
    ├── evening-preview.png  # 晚礼服预览
    └── cute-preview.png     # 可爱风预览
```

## 图片要求

### 看板娘完整形象 (mascot/)
- 尺寸：建议 400x400 像素或更高
- 格式：PNG（支持透明背景）
- 内容：看板娘穿着对应服装的完整形象
- 背景：透明或纯色背景

### 服装预览图 (outfits/)
- 尺寸：建议 200x200 像素
- 格式：PNG（支持透明背景）
- 内容：服装的局部特写或图标
- 用途：在服装选择网格中展示

## 功能说明

1. **响应式布局**：自适应电脑和手机端
2. **服装切换**：点击服装预览图可实时更换看板娘形象
3. **选中状态**：当前选中的服装会有特殊高亮效果
4. **本地存储**：用户选择的服装会保存到本地存储
5. **返回功能**：左上角返回按钮可回到首页

## 页面路由
- 页面路径：`/pages/dress-up/dress-up`
- 从首页进入：点击"看板娘换装"卡片

## 开发说明
- 如果图片资源暂时缺失，页面会使用默认图片
- 可以在 `dress-up.vue` 中的 `outfits` 数组添加更多服装配置
- 支持自定义服装名称和图片路径
