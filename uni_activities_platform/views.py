from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage!")  # 간단한 환영 메시지 출력
