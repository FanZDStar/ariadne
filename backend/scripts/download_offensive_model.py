"""
下载冒犯性内容检测模型到本地项目

运行方式:
cd backend
python scripts/download_offensive_model.py

模型将被保存到: backend/models/offensive_detector/
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def download_model():
    """下载模型到本地项目目录"""
    
    print("=" * 70)
    print("🚀 开始下载冒犯性内容检测模型")
    print("=" * 70)
    print()
    
    # 设置模型保存路径（项目本地）
    backend_dir = Path(__file__).parent.parent
    model_dir = backend_dir / "models" / "offensive_detector"
    
    print(f"📁 模型将保存到: {model_dir}")
    print()
    
    # 创建目录
    model_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        model_name = "thu-coai/roberta-base-cold"
        
        print(f"⏬ 正在下载模型: {model_name}")
        print("   首次下载约 400MB，可能需要几分钟...")
        print()
        
        # 下载分词器
        print("📦 [1/2] 下载分词器 (Tokenizer)...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=str(model_dir)
        )
        print("✅ 分词器下载完成")
        print()
        
        # 下载模型
        print("📦 [2/2] 下载模型 (Model)...")
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            cache_dir=str(model_dir)
        )
        print("✅ 模型下载完成")
        print()
        
        # 保存到本地
        print("💾 保存模型到本地...")
        local_model_path = model_dir / "local_model"
        tokenizer.save_pretrained(str(local_model_path))
        model.save_pretrained(str(local_model_path))
        print(f"✅ 模型已保存到: {local_model_path}")
        print()
        
        # 验证模型
        print("🧪 验证模型...")
        test_text = "测试文本"
        inputs = tokenizer(test_text, return_tensors="pt")
        outputs = model(**inputs)
        print("✅ 模型验证成功")
        print()
        
        print("=" * 70)
        print("🎉 模型下载完成！")
        print("=" * 70)
        print()
        print("📝 使用说明:")
        print(f"   1. 模型位置: {local_model_path}")
        print("   2. 服务会自动使用本地模型（无需修改代码）")
        print("   3. 可以删除系统缓存目录中的模型以节省空间")
        print()
        print("🗑️  可选：删除系统缓存（节省空间）")
        if sys.platform == "win32":
            cache_path = Path.home() / ".cache" / "huggingface"
        else:
            cache_path = Path.home() / ".cache" / "huggingface"
        print(f"   系统缓存位置: {cache_path}")
        print()
        
        return True
        
    except ImportError:
        print("❌ 错误: 缺少依赖库")
        print("   请先运行: pip install transformers torch")
        return False
        
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        print()
        print("💡 常见问题解决:")
        print("   1. 网络连接问题 - 使用国内镜像:")
        print("      export HF_ENDPOINT=https://hf-mirror.com")
        print("   2. 磁盘空间不足 - 需要至少 1GB 空闲空间")
        print("   3. 依赖问题 - pip install transformers torch")
        return False


def check_model_exists():
    """检查模型是否已存在"""
    backend_dir = Path(__file__).parent.parent
    model_path = backend_dir / "models" / "offensive_detector" / "local_model"
    
    if model_path.exists() and (model_path / "config.json").exists():
        print("📦 检测到本地已有模型")
        print(f"   位置: {model_path}")
        print()
        
        # 询问是否重新下载
        response = input("是否重新下载模型？(y/N): ").strip().lower()
        if response not in ['y', 'yes', '是']:
            print("✅ 使用现有模型")
            return True
    
    return False


def show_model_info():
    """显示模型信息"""
    backend_dir = Path(__file__).parent.parent
    model_dir = backend_dir / "models" / "offensive_detector"
    
    if not model_dir.exists():
        print("ℹ️  模型尚未下载")
        return
    
    # 计算目录大小
    total_size = 0
    file_count = 0
    for file in model_dir.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
            file_count += 1
    
    print()
    print("=" * 70)
    print("📊 本地模型信息")
    print("=" * 70)
    print(f"   位置: {model_dir}")
    print(f"   文件数: {file_count}")
    print(f"   总大小: {total_size / (1024**2):.1f} MB")
    print("=" * 70)
    print()


if __name__ == "__main__":
    print()
    
    # 检查是否已有模型
    if check_model_exists():
        show_model_info()
        sys.exit(0)
    
    # 下载模型
    success = download_model()
    
    if success:
        show_model_info()
        sys.exit(0)
    else:
        sys.exit(1)
