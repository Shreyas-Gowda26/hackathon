from fastapi import Depends,HTTPException,status
from hackathon.auth.oauth2 import get_current_user


def allow_roles(*allowed_roles):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = f"Access forbidden for role: {user_role}"
            )
        return current_user
    return role_checker

