# file:ariadne/backend/app/api/routes/tree_hole.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from pydantic import ValidationError
from sqlalchemy import and_, func
from typing import List
import json
from app.database.session import get_db
from app.models.user import User
from app.models.tree_hole_chat import TreeHoleChatParticipant
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment, TreeHoleLike, UserWhisperInteraction
from app.schemas.tree_hole import (
    WhisperCreate,
    WhisperUpdate,
    WhisperResponse,
    CommentResponse,
    CommentCreate,
    LikeWithStarResponse,
    CommentWithStarResponse,
    WhisperWithStarResponse,
    StarRewardInfo,
)
from app.api.deps import get_current_user
from app.services.star_point_service import StarPointService
from app.utils.star_point_types import StarPointAction, SourceType
from app.services.offensive_content_detector import check_offensive_content

router = APIRouter(prefix="/tree-hole", tags=["心灵树洞"])


@router.post(
    "/", response_model=WhisperWithStarResponse, status_code=status.HTTP_201_CREATED
)
def create_whisper(
    whisper: WhisperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建新的悄悄话"""
    from app.models.tree_hole import TreeHoleWhisperImage

    # 创建悄悄话对象
    db_whisper = TreeHoleWhisper(
        user_id=current_user.user_id,
        title=whisper.title,
        mood=whisper.mood,
        tags=whisper.tags,
        is_anonymous=whisper.is_anonymous,
        anonymous_name=whisper.anonymous_name,
        anonymous_avatar=whisper.anonymous_avatar,
    )

    # 使用加密属性设置内容，自动处理加密
    db_whisper.decrypted_content = whisper.content

    db.add(db_whisper)
    db.commit()
    db.refresh(db_whisper)

    # 创建关联的图片记录
    if whisper.images:
        for image_data in whisper.images:
            db_image = TreeHoleWhisperImage(
                whisper_id=db_whisper.whisper_id,
                image_url=image_data.image_url,
                image_order=image_data.image_order,
            )
            db.add(db_image)
        db.commit()
        db.refresh(db_whisper)

    # 确保返回解密后的内容
    db_whisper.content = db_whisper.decrypted_content

    # 处理星点奖励 - 每日第一次发表悄悄话获得2星点
    star_reward = StarRewardInfo()
    try:
        star_service = StarPointService(db)
        award_result = star_service.award_points(
            user_id=current_user.user_id,
            action=StarPointAction.TREE_HOLE_WHISPER,
            source_type=SourceType.TREE_HOLE,
            source_id=str(db_whisper.whisper_id),
        )

        if award_result.rewarded:
            star_reward = StarRewardInfo(
                earned_points=award_result.points_awarded,
                is_rewarded=True,
                action_type=StarPointAction.TREE_HOLE_WHISPER.value,
                description=f"发表悄悄话获得{award_result.points_awarded}星点",
            )
            print(f"⭐ 悄悄话奖励成功: {award_result.points_awarded}星点")
        else:
            print(f"⭐ 悄悄话奖励: {award_result.message}")
    except Exception as e:
        print(f"❌ 悄悄话奖励失败: {str(e)}")

    # 创建带星点奖励信息的响应
    whisper_data = {
        "whisper_id": db_whisper.whisper_id,
        "content": db_whisper.content,  # 已经是解密后的内容
        "user_id": db_whisper.user_id,
        "like_count": db_whisper.like_count,
        "comment_count": db_whisper.comment_count,
        "is_anonymous": db_whisper.is_anonymous,
        "created_at": db_whisper.created_at,
        "updated_at": db_whisper.updated_at,
        "user": (
            {
                "user_id": db_whisper.user.user_id,
                "username": db_whisper.user.username,
                "nickname": db_whisper.user.nickname,
                "avatar_url": db_whisper.user.avatar_url,
                "email": db_whisper.user.email,
                "bio": db_whisper.user.bio,
                "created_at": db_whisper.user.created_at,
                "is_active": db_whisper.user.is_active,
            }
            if db_whisper.user
            else None
        ),
        "images": (
            [
                {
                    "image_url": img.image_url,
                    "image_order": img.image_order,
                    "image_id": img.image_id,
                    "whisper_id": img.whisper_id,
                    "created_at": img.created_at,
                }
                for img in db_whisper.images
            ]
            if db_whisper.images
            else []
        ),
        "liked": False,  # 自己发的悄悄话默认未点赞
        "star_reward": star_reward,
    }

    result = WhisperWithStarResponse(**whisper_data)
    return result


@router.get("/my-whispers", response_model=List[WhisperResponse])
def get_user_whispers(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有悄悄话，按时间倒序排列"""
    whispers = (
        db.query(TreeHoleWhisper)
        .options(joinedload(TreeHoleWhisper.user), joinedload(TreeHoleWhisper.images))
        .filter(TreeHoleWhisper.user_id == current_user.user_id)
        .order_by(TreeHoleWhisper.created_at.desc())
        .all()
    )

    for whisper in whispers:
        like = (
            db.query(TreeHoleLike)
            .filter(
                TreeHoleLike.whisper_id == whisper.whisper_id,
                TreeHoleLike.user_id == current_user.user_id,
            )
            .first()
        )
        whisper.liked = like is not None

        # 计算该悄悄话的实际评论数（从 TreeHoleComment 表）
        actual_comment_count = (
            db.query(TreeHoleComment)
            .filter(TreeHoleComment.whisper_id == whisper.whisper_id)
            .count()
        )

        # 更新数据库中的 comment_count 字段以保持同步
        if whisper.comment_count != actual_comment_count:
            whisper.comment_count = actual_comment_count

        # 确保返回解密后的内容
        whisper.content = whisper.decrypted_content

    return whispers


@router.get("/random", response_model=WhisperResponse)
def get_random_whisper(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """随机获取一个悄悄话"""
    whisper = (
        db.query(TreeHoleWhisper)
        .options(joinedload(TreeHoleWhisper.user), joinedload(TreeHoleWhisper.images))
        .filter(TreeHoleWhisper.user_id != current_user.user_id)
        .order_by(func.rand())
        .first()
    )

    if not whisper:
        raise HTTPException(status_code=404, detail="No whispers found")

    like = (
        db.query(TreeHoleLike)
        .filter(
            TreeHoleLike.whisper_id == whisper.whisper_id,
            TreeHoleLike.user_id == current_user.user_id,
        )
        .first()
    )
    whisper.liked = like is not None

    # 确保返回解密后的内容
    whisper.content = whisper.decrypted_content

    return whisper


@router.get("/", response_model=List[WhisperResponse])
def get_public_whispers(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取公开的悄悄话（用于做倾听者功能）"""
    whispers = (
        db.query(TreeHoleWhisper)
        .options(joinedload(TreeHoleWhisper.user), joinedload(TreeHoleWhisper.images))
        .filter(TreeHoleWhisper.is_anonymous == True)
        .order_by(TreeHoleWhisper.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    for whisper in whispers:
        like = (
            db.query(TreeHoleLike)
            .filter(
                TreeHoleLike.whisper_id == whisper.whisper_id,
                TreeHoleLike.user_id == current_user.user_id,
            )
            .first()
        )
        whisper.liked = like is not None

        # 确保返回解密后的内容
        whisper.content = whisper.decrypted_content

    return whispers


@router.get("/my-interactions", response_model=List[WhisperResponse])
def get_user_interactions(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取用户参与互动的悄悄话（点赞或评论过的）
    基于 user_whisper_interactions 表，只返回 is_active=True 的互动记录
    排除自己的悄悄话，按最后互动时间倒序
    """

    # 1) 先把候选 whisper 批量查出（带必要的关系）
    whispers: list[TreeHoleWhisper] = (
        db.query(TreeHoleWhisper)
        .options(
            joinedload(TreeHoleWhisper.user),
            joinedload(TreeHoleWhisper.images),
        )
        .join(
            UserWhisperInteraction,
            TreeHoleWhisper.whisper_id == UserWhisperInteraction.whisper_id,
        )
        .filter(UserWhisperInteraction.user_id == current_user.user_id)
        .filter(UserWhisperInteraction.is_active.is_(True))
        .filter(TreeHoleWhisper.user_id != current_user.user_id)
        .order_by(UserWhisperInteraction.last_interaction_at.desc())
        .all()
    )

    if not whispers:
        return []

    whisper_ids = [w.whisper_id for w in whispers]

    # 2) 批量查点赞（当前用户是否点过赞）
    liked_id_set: set[int] = {
        wid
        for (wid,) in (
            db.query(TreeHoleLike.whisper_id)
            .filter(TreeHoleLike.user_id == current_user.user_id)
            .filter(TreeHoleLike.whisper_id.in_(whisper_ids))
            .all()
        )
    }

    # 3) 批量查评论数
    comment_count_map: dict[int, int] = {
        wid: cnt
        for wid, cnt in (
            db.query(TreeHoleComment.whisper_id, func.count(TreeHoleComment.comment_id))
            .filter(TreeHoleComment.whisper_id.in_(whisper_ids))
            .group_by(TreeHoleComment.whisper_id)
            .all()
        )
    }

    # 4) 批量查互动记录（决定 interaction_type）
    #    注意：同一个 user_id + whisper_id 唯一
    interaction_map: dict[int, str] = {}
    interactions: list[UserWhisperInteraction] = (
        db.query(UserWhisperInteraction)
        .filter(UserWhisperInteraction.user_id == current_user.user_id)
        .filter(UserWhisperInteraction.whisper_id.in_(whisper_ids))
        .filter(UserWhisperInteraction.is_active.is_(True))
        .all()
    )

    for it in interactions:
        if it.has_liked and it.has_commented:
            interaction_map[it.whisper_id] = "both"
        elif it.has_liked:
            interaction_map[it.whisper_id] = "like"
        elif it.has_commented:
            interaction_map[it.whisper_id] = "comment"
        else:
            # 没有任何有效互动就不放（等价于 None）
            pass

    # 5) 逐条构造 WhisperResponse（而不是返回 ORM 实例）
    items: list[WhisperResponse] = []
    for idx, w in enumerate(whispers):
        has_like = w.whisper_id in liked_id_set
        actual_comment_count = comment_count_map.get(w.whisper_id, 0)
        interaction_type = interaction_map.get(w.whisper_id)

        # 这里直接用 dict + model_validate，from_attributes=True 允许子对象仍用 ORM
        payload = {
             # —— WhisperBase 必需/常用字段 ——
            "title": w.title,
            "content": w.decrypted_content,        # ⭐ 必填 + 解密
            "mood": (w.mood.value if w.mood else None),  # 跨枚举，传字符串更稳
            "tags": w.tags,
            "is_anonymous": w.is_anonymous,
            "anonymous_name": w.anonymous_name,
            "anonymous_avatar": w.anonymous_avatar,
            
            "whisper_id": w.whisper_id,
            "user_id": w.user_id,
            "like_count": w.like_count,           # 假设表里有 like_count 聚合列
            "comment_count": actual_comment_count, # 用我们批量统计的真实评论数
            "created_at": w.created_at,
            "updated_at": w.updated_at,
            "user": w.user,                        # ORM：交给 from_attributes 处理
            "images": w.images,                    # ORM 列表：同上
            "liked": has_like,
            "interaction_type": interaction_type,
        }
        item = WhisperResponse.model_validate(payload, from_attributes=True)
        items.append(item)

    return items

@router.get("/{whisper_id}", response_model=WhisperResponse)
def get_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取特定的悄悄话"""
    try:
        whisper = (
            db.query(TreeHoleWhisper)
            .options(
                joinedload(TreeHoleWhisper.user), joinedload(TreeHoleWhisper.images)
            )
            .filter(TreeHoleWhisper.whisper_id == whisper_id)
            .first()
        )

        if not whisper:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Whisper not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 查询悄悄话失败 #{whisper_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"加载悄悄话失败: {str(e)}",
        )

    # 权限检查：
    # 所有登录用户都可以查看悄悄话详情（用于评论功能）
    # 隐私通过匿名机制保护，而不是访问限制
    # 注：原先的严格权限检查会阻止用户从"倾听者"页面进入详情页评论
    
    # 如果是非匿名且非本人的悄悄话，只返回必要信息，隐藏敏感内容
    # （当前实现中，敏感内容已通过匿名机制处理，这里保持原有逻辑）
    
    # 移除了过于严格的权限检查，允许所有登录用户查看
    # 原代码要求：是匿名/是创建者/点赞过/参与聊天/评论过，才能访问
    # 新逻辑：只要登录即可访问（已通过 get_current_user 验证）

    like = (
        db.query(TreeHoleLike)
        .filter(
            TreeHoleLike.whisper_id == whisper.whisper_id,
            TreeHoleLike.user_id == current_user.user_id,
        )
        .first()
    )
    whisper.liked = like is not None

    # 确保返回解密后的内容
    whisper.content = whisper.decrypted_content

    return whisper


@router.put("/{whisper_id}", response_model=WhisperResponse)
def update_whisper(
    whisper_id: int,
    whisper_update: WhisperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新悄悄话"""
    db_whisper = (
        db.query(TreeHoleWhisper)
        .options(joinedload(TreeHoleWhisper.images))
        .filter(TreeHoleWhisper.whisper_id == whisper_id)
        .filter(TreeHoleWhisper.user_id == current_user.user_id)
        .first()
    )

    if not db_whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Whisper not found"
        )

    # 更新字段
    update_data = whisper_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "content":
            # 对于内容字段，使用加密属性
            db_whisper.decrypted_content = value
        else:
            setattr(db_whisper, key, value)

    db.commit()
    db.refresh(db_whisper)

    # 确保返回解密后的内容
    db_whisper.content = db_whisper.decrypted_content
    return db_whisper


@router.delete("/{whisper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除悄悄话"""
    db_whisper = (
        db.query(TreeHoleWhisper)
        .filter(TreeHoleWhisper.whisper_id == whisper_id)
        .filter(TreeHoleWhisper.user_id == current_user.user_id)
        .first()
    )

    if not db_whisper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Whisper not found"
        )

    db.delete(db_whisper)
    db.commit()
    return


@router.post("/{whisper_id}/like", response_model=LikeWithStarResponse)
def like_whisper(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """点赞悄悄话"""
    db_whisper = (
        db.query(TreeHoleWhisper)
        .filter(TreeHoleWhisper.whisper_id == whisper_id)
        .first()
    )
    if not db_whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    like = (
        db.query(TreeHoleLike)
        .filter(
            TreeHoleLike.whisper_id == whisper_id,
            TreeHoleLike.user_id == current_user.user_id,
        )
        .first()
    )

    is_liked = False
    if like:
        # 取消点赞
        db.delete(like)
        db_whisper.like_count -= 1
        
        # 更新互动记录：取消点赞状态（但不删除互动记录）
        if db_whisper.user_id != current_user.user_id:  # 不记录自己的悄悄话
            interaction = db.query(UserWhisperInteraction).filter(
                UserWhisperInteraction.user_id == current_user.user_id,
                UserWhisperInteraction.whisper_id == whisper_id
            ).first()
            if interaction:
                interaction.has_liked = False
                interaction.last_interaction_at = func.now()
    else:
        # 点赞
        new_like = TreeHoleLike(whisper_id=whisper_id, user_id=current_user.user_id)
        db.add(new_like)
        db_whisper.like_count += 1
        is_liked = True
        
        # 创建或更新互动记录（不记录自己对自己悄悄话的互动）
        if db_whisper.user_id != current_user.user_id:
            interaction = db.query(UserWhisperInteraction).filter(
                UserWhisperInteraction.user_id == current_user.user_id,
                UserWhisperInteraction.whisper_id == whisper_id
            ).first()
            
            if interaction:
                # 更新已有互动记录
                interaction.has_liked = True
                interaction.is_active = True  # 重新激活
                interaction.last_interaction_at = func.now()
            else:
                # 创建新互动记录
                new_interaction = UserWhisperInteraction(
                    user_id=current_user.user_id,
                    whisper_id=whisper_id,
                    has_liked=True,
                    has_commented=False
                )
                db.add(new_interaction)

    db.commit()

    # 处理星点奖励 - 每日前三次互动（点赞）获得1星点
    star_reward = StarRewardInfo()
    if is_liked:  # 只有点赞（不是取消点赞）时才给奖励
        try:
            star_service = StarPointService(db)
            award_result = star_service.award_points(
                user_id=current_user.user_id,
                action=StarPointAction.TREE_HOLE_INTERACTION,
                source_type=SourceType.TREE_HOLE,
                source_id=str(whisper_id),
            )

            if award_result.rewarded:
                star_reward = StarRewardInfo(
                    earned_points=award_result.points_awarded,
                    is_rewarded=True,
                    action_type=StarPointAction.TREE_HOLE_INTERACTION.value,
                    description=f"点赞获得{award_result.points_awarded}星点",
                )
                print(f"⭐ 点赞奖励成功: {award_result.points_awarded}星点")
            else:
                print(f"⭐ 点赞奖励: {award_result.message}")
        except Exception as e:
            print(f"❌ 点赞奖励失败: {str(e)}")

    return LikeWithStarResponse(
        message="操作成功", liked=is_liked, star_reward=star_reward
    )





@router.delete("/my-interactions/{whisper_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_interaction_link(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """移除互动链接（仅标记为无效，不删除原悄悄话和点赞/评论记录）
    
    类似Windows快捷方式，删除的只是指向悄悄话的链接，不影响原悄悄话本身
    """
    # 查找互动记录
    interaction = db.query(UserWhisperInteraction).filter(
        UserWhisperInteraction.user_id == current_user.user_id,
        UserWhisperInteraction.whisper_id == whisper_id
    ).first()
    
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    
    # 标记为无效（软删除）
    interaction.is_active = False
    db.commit()
    
    return


@router.get("/{whisper_id}/comments", response_model=List[CommentResponse])
def get_whisper_comments(
    whisper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取悄悄话的评论列表"""
    # 先检查悄悄话是否存在
    whisper = (
        db.query(TreeHoleWhisper)
        .filter(TreeHoleWhisper.whisper_id == whisper_id)
        .first()
    )
    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    # 获取评论列表
    comments = (
        db.query(TreeHoleComment)
        .options(joinedload(TreeHoleComment.user))
        .filter(TreeHoleComment.whisper_id == whisper_id)
        .order_by(TreeHoleComment.created_at.desc())
        .all()
    )

    # 构造评论响应数据
    comment_list = []
    for comment in comments:
        comment_dict = {
            "comment_id": comment.comment_id,
            "whisper_id": comment.whisper_id,
            "user_id": comment.user_id,
            "content": comment.decrypted_content,
            "is_anonymous": comment.is_anonymous,
            "created_at": comment.created_at,
            "user": comment.user,
        }
        comment_list.append(comment_dict)

    return comment_list


@router.post("/{whisper_id}/comments", response_model=CommentWithStarResponse)
def create_whisper_comment(
    whisper_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建悄悄话评论"""
    # 检查悄悄话是否存在
    whisper = (
        db.query(TreeHoleWhisper)
        .filter(TreeHoleWhisper.whisper_id == whisper_id)
        .first()
    )
    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")

    # 🛡️ 冒犯性内容检测（AI模型 + 关键词黑名单）
    try:
        detection_result = check_offensive_content(comment_data.content, threshold=0.5)
        
        if detection_result["is_offensive"]:
            # 检测到冒犯性内容，拒绝发布
            error_message = detection_result["message"]
            
            # 如果是关键词匹配，提供更明确的提示
            if detection_result.get("matched_keyword"):
                error_message = f"评论包含敏感词「{detection_result['matched_keyword']}」，请文明发言"
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "offensive_content_detected",
                    "message": error_message,
                    "confidence": detection_result["confidence"],
                    "matched_keyword": detection_result.get("matched_keyword")
                }
            )
    except HTTPException:
        # 重新抛出 HTTPException
        raise
    except Exception as e:
        # 检测服务异常时记录日志但允许评论通过
        print(f"⚠️ 冒犯性内容检测异常: {str(e)}")

    # 创建评论
    db_comment = TreeHoleComment(
        whisper_id=whisper_id,
        user_id=current_user.user_id,
        is_anonymous=comment_data.is_anonymous,
    )

    # 设置加密内容
    db_comment.decrypted_content = comment_data.content

    db.add(db_comment)

    # 更新悄悄话的评论数
    whisper.comment_count += 1
    
    # 创建或更新互动记录（不记录自己对自己悄悄话的互动）
    if whisper.user_id != current_user.user_id:
        interaction = db.query(UserWhisperInteraction).filter(
            UserWhisperInteraction.user_id == current_user.user_id,
            UserWhisperInteraction.whisper_id == whisper_id
        ).first()
        
        if interaction:
            # 更新已有互动记录
            interaction.has_commented = True
            interaction.is_active = True  # 重新激活
            interaction.last_interaction_at = func.now()
        else:
            # 创建新互动记录
            new_interaction = UserWhisperInteraction(
                user_id=current_user.user_id,
                whisper_id=whisper_id,
                has_liked=False,
                has_commented=True
            )
            db.add(new_interaction)

    db.commit()
    db.refresh(db_comment)

    # 处理星点奖励 - 每日前三次互动（评论）获得1星点
    star_reward = StarRewardInfo()
    try:
        star_service = StarPointService(db)
        award_result = star_service.award_points(
            user_id=current_user.user_id,
            action=StarPointAction.TREE_HOLE_INTERACTION,
            source_type=SourceType.TREE_HOLE,
            source_id=str(whisper_id),
        )

        if award_result.rewarded:
            star_reward = StarRewardInfo(
                earned_points=award_result.points_awarded,
                is_rewarded=True,
                action_type=StarPointAction.TREE_HOLE_INTERACTION.value,
                description=f"评论获得{award_result.points_awarded}星点",
            )
            print(f"⭐ 评论奖励成功: {award_result.points_awarded}星点")
        else:
            print(f"⭐ 评论奖励: {award_result.message}")
    except Exception as e:
        print(f"❌ 评论奖励失败: {str(e)}")

    return CommentWithStarResponse(
        message="评论创建成功",
        comment_id=db_comment.comment_id,
        star_reward=star_reward,
    )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_whisper_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除悄悄话评论
    
    权限：
    - 悄悄话发布者可以删除任意评论
    - 评论发布者只能删除自己的评论
    """
    # 查找评论
    comment = db.query(TreeHoleComment).filter(
        TreeHoleComment.comment_id == comment_id
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # 查找对应的悄悄话
    whisper = db.query(TreeHoleWhisper).filter(
        TreeHoleWhisper.whisper_id == comment.whisper_id
    ).first()
    
    if not whisper:
        raise HTTPException(status_code=404, detail="Whisper not found")
    
    # 权限检查：是悄悄话发布者或评论发布者
    is_whisper_author = whisper.user_id == current_user.user_id
    is_comment_author = comment.user_id == current_user.user_id
    
    if not (is_whisper_author or is_comment_author):
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to delete this comment"
        )
    
    # 删除评论
    db.delete(comment)
    
    # 更新悄悄话的评论数
    if whisper.comment_count > 0:
        whisper.comment_count -= 1
    
    db.commit()
    
    return None


@router.post("/reset-comment-counts")
def reset_comment_counts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    重置所有悄悄话的评论数量（管理员功能）
    先将所有 comment_count 重置为0，然后根据实际评论数重新计算
    """
    try:
        # 获取所有悄悄话
        whispers = db.query(TreeHoleWhisper).all()
        total_whispers = len(whispers)

        # 第一步：重置所有评论数为0
        for whisper in whispers:
            whisper.comment_count = 0
        db.commit()

        # 第二步：根据实际评论重新计算
        updated_count = 0
        has_comments = 0
        results = []

        for whisper in whispers:
            # 统计实际的评论数
            actual_comment_count = (
                db.query(TreeHoleComment)
                .filter(TreeHoleComment.whisper_id == whisper.whisper_id)
                .count()
            )

            # 更新评论数
            if actual_comment_count > 0:
                whisper.comment_count = actual_comment_count
                results.append(
                    {
                        "whisper_id": whisper.whisper_id,
                        "comment_count": actual_comment_count,
                    }
                )
                has_comments += 1
                updated_count += actual_comment_count

        # 提交更改
        db.commit()

        return {
            "message": "重置并同步完成",
            "total_whispers": total_whispers,
            "whispers_with_comments": has_comments,
            "whispers_without_comments": total_whispers - has_comments,
            "total_comments": updated_count,
            "details": results,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"重置失败: {str(e)}")


@router.post("/sync-comment-counts")
def sync_comment_counts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    同步所有悄悄话的评论数量（管理员功能）
    将 comment_count 字段更新为实际的评论数量（不会重置为0）
    """
    try:
        # 获取所有悄悄话
        whispers = db.query(TreeHoleWhisper).all()

        updated_count = 0
        results = []

        for whisper in whispers:
            # 统计实际的评论数
            actual_comment_count = (
                db.query(TreeHoleComment)
                .filter(TreeHoleComment.whisper_id == whisper.whisper_id)
                .count()
            )

            # 如果数量不一致，则更新
            if whisper.comment_count != actual_comment_count:
                old_count = whisper.comment_count
                whisper.comment_count = actual_comment_count
                results.append(
                    {
                        "whisper_id": whisper.whisper_id,
                        "old_count": old_count,
                        "new_count": actual_comment_count,
                    }
                )
                updated_count += 1

        # 提交更改
        db.commit()

        return {
            "message": "同步完成",
            "total_whispers": len(whispers),
            "updated_count": updated_count,
            "details": results,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")
