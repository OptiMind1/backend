from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    읽기 권한은 모두 허용하되,
    수정 및 삭제는 작성자에게만 허용.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 객체의 작성자와 현재 요청한 유저가 같아야 수정/삭제 가능
        return obj.author == request.user
