import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv() 

# API base URL
BASE_URL = "http://localhost:8000"

def sign_up(email, password, full_name):
    url = f"{BASE_URL}/auth/signup"
    data = {
        "credentials": {"email": email, "password": password},
        "profile": {"full_name": full_name}
    }
    response = requests.post(url, json=data)
    return response.json()

def sign_in(email, password):
    url = f"{BASE_URL}/auth/signin"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def sign_out(access_token):
    url = f"{BASE_URL}/auth/signout"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    return response.json()

def create_blog_post(title, content, author_id, access_token):
    url = f"{BASE_URL}/blog/posts"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": title,
        "content": content,
        "author_id": author_id
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def update_blog_post(post_id, title, content, access_token):
    url = f"{BASE_URL}/blog/posts/{post_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": title,
        "content": content
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

def get_user_profile(user_id, access_token):
    url = f"{BASE_URL}/auth/profile/{user_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def update_user_profile(user_id, full_name, avatar_url, access_token):
    url = f"{BASE_URL}/auth/profile/{user_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "full_name": full_name,
        "avatar_url": avatar_url
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

def create_user_profile(user_id, full_name, avatar_url, access_token):
    url = f"{BASE_URL}/auth/profile/{user_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "full_name": full_name,
        "avatar_url": avatar_url
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Sign up a new user
    email = "tommasominuto@gmail.com"
    password = "2000tommy"
    full_name = "Test User"
    
    signup_result = sign_up(email, password, full_name)
    print("Sign up result:", json.dumps(signup_result, indent=2))

    # Sign in the user
    signin_result = sign_in(email, password)
    print("Sign in result:", json.dumps(signin_result, indent=2))

    if "access_token" in signin_result:
        access_token = signin_result["access_token"]
        user_id = signin_result["user"]["id"]

        # Get user profile
        user_profile = get_user_profile(user_id, access_token)
        print("User profile:", json.dumps(user_profile, indent=2))

        # Update user profile
        updated_profile = update_user_profile(
            user_id=user_id,
            full_name="Updated Test User",
            avatar_url="https://example.com/avatar.jpg",
            access_token=access_token
        )
        print("Updated user profile:", json.dumps(updated_profile, indent=2))

        # Get updated user profile
        updated_user_profile = get_user_profile(user_id, access_token)
        print("Updated user profile (fetched):", json.dumps(updated_user_profile, indent=2))

        # Create a blog post
        blog_post = create_blog_post(
            title="My First Blog Post",
            content="This is the content of my first blog post.",
            author_id=user_id,
            access_token=access_token
        )
        print("Blog post created:", json.dumps(blog_post, indent=2))

        # Update the blog post
        updated_post = update_blog_post(
            post_id=blog_post["id"],
            title="Updated Blog Post Title",
            content="This is the updated content of my first blog post.",
            access_token=access_token
        )
        print("Blog post updated:", json.dumps(updated_post, indent=2))

        # Sign out the user
        signout_result = sign_out(access_token)
        print("Sign out result:", json.dumps(signout_result, indent=2))
    else:
        print("Failed to sign in or retrieve access token")
