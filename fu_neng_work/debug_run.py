# gen_models.py
import subprocess
import os

if __name__ == "__main__":
    # 定义固定参数
    source = r"D:\code\python_project\aomaker_test\fu_neng_work\data\api_data\template_save.json"
    output = os.path.normpath(r".\maker\apis")  # 路径规范化
    custom_script = ""

    # 执行命令
    try:
        subprocess.run(
            ["aomaker", "gen", "models",
             "-s", source,
             "-o", output,
             "-cs", custom_script],
            check=True
        )
        print("✅ 生成成功")
    except subprocess.CalledProcessError:
        print("❌ 生成失败，请检查：")
        print(f"1. 确保文件存在: {source}")
        print(f"2. 验证输出目录: {output}")
        print(f"3. 确认命名配置: {custom_script}")
    except FileNotFoundError:
        print("⚠️  未找到aomaker命令，请先安装或将其加入PATH环境变量")