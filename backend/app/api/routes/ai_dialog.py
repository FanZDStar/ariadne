from fastapi import APIRouter, Request
from pydantic import BaseModel
import httpx
from app.core.config import settings

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class DialogRequest(BaseModel):
    messages: list[Message]
    system_prompt: str | None = None

class DialogResponse(BaseModel):
    content: str

# 默认AI参数，可根据需要调整
AI_API_URL = getattr(settings, "ai_api_url", "https://api.suanli.cn/v1/chat/completions")
AI_API_KEY = getattr(settings, "ai_api_key", "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo")
AI_MODEL = getattr(settings, "ai_model", "free:Qwen3-30B-A3B")

@router.post("/ai-dialog", response_model=DialogResponse)
async def ai_dialog(data: DialogRequest, request: Request):
    # 构造请求体
    payload = {
        "model": AI_MODEL,
        "messages": [],
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.9
    }
    # 系统提示词优先用前端传递，否则用默认
    if data.system_prompt:
        payload["messages"].append({"role": "system", "content": data.system_prompt})
    # 添加历史对话
    for msg in data.messages[-8:]:
        payload["messages"].append({"role": msg.role if msg.role != "ai" else "assistant", "content": msg.content})
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                AI_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {AI_API_KEY}"
                },
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("choices") and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                # 内容优化过滤
                optimized = optimize_ai_response(content)
                return DialogResponse(content=optimized)
            else:
                return DialogResponse(content="AI响应异常，请稍后再试。")
        except Exception as e:
            return DialogResponse(content=f"AI服务异常: {str(e)}")

# AI回复内容优化，去除标签、无关信息，保证体验
def optimize_ai_response(content: str) -> str:
    import re
    optimized = re.sub(r"<think>[\s\S]*?</think>", "", content)
    optimized = re.sub(r"<think>[\s\S]*", "", optimized)
    optimized = re.sub(r"我不想展示.*?因为这会影响用户体验", "", optimized)
    optimized = re.sub(r"^(AI|助手|阿德涅)[:：]\s*", "", optimized)
    optimized = re.sub(r"^(我是|作为)[^，。]*[，。]\s*", "", optimized)
    optimized = re.sub(r"\[.*?\]", "", optimized)
    optimized = re.sub(r"（.*?思考.*?）", "", optimized)
    optimized = re.sub(r"\*.*?思考.*?\*", "", optimized)
    optimized = re.sub(r"【.*?】", "", optimized)
    optimized = re.sub(r"^\s*[-*•]\s*", "", optimized, flags=re.MULTILINE)
    optimized = re.sub(r"\n\s*\n", "\n", optimized)
    optimized = optimized.strip()
    if len(optimized) < 20:
        optimized = "我理解你的感受。能告诉我更多关于这个情况的细节吗？这样我能更好地陪伴你进行这场自我对话。"
    if len(optimized) > 500:
        optimized = optimized[:500] + "..."
    if not optimized or len(optimized) < 5:
        optimized = "我正在认真思考你的话。你能再详细说说这个情况吗？我想更好地理解你的感受。"
    return optimized
