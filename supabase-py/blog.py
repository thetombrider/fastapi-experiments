from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from supabase import Client
from database import get_supabase

router = APIRouter()

# Pydantic models for blog posts
class BlogPostCreate(BaseModel):
    title: str
    content: str
    author_id: str

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogPost(BlogPostCreate):
    id: int
    created_at: str

# Blog post endpoints
@router.post("/posts", response_model=BlogPost)
async def create_post(post: BlogPostCreate, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table('blog_posts').insert(post.dict()).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating post: {str(e)}")

@router.get("/posts", response_model=List[BlogPost])
async def get_posts(supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table('blog_posts').select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching posts: {str(e)}")

@router.get("/posts/{post_id}", response_model=BlogPost)
async def get_post(post_id: int, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table('blog_posts').select("*").eq('id', post_id).execute()
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching post: {str(e)}")

@router.put("/posts/{post_id}", response_model=BlogPost)
async def update_post(post_id: int, post_update: BlogPostUpdate, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table('blog_posts').update(post_update.dict(exclude_unset=True)).eq('id', post_id).execute()
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating post: {str(e)}")

@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int, supabase: Client = Depends(get_supabase)):
    try:
        response = supabase.table('blog_posts').delete().eq('id', post_id).execute()
        if response.data:
            return {"message": "Post deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting post: {str(e)}")
