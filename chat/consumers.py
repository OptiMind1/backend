import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chat.translate import translate_text
from django_ratelimit.decorators import ratelimit
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    @ratelimit(key='user', rate='10/m', method='ALL', burst=True)
    async def connect(self):
        # WebSocket 연결 시 room_name을 URL에서 가져와서 사용
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

         # 쿼리 파라미터에서 언어 가져오기
        query_string = parse_qs(self.scope['query_string'].decode())
        self.user_lang = query_string.get('lang', ['en'])[0]  # 기본값 영어

        # 해당 그룹에 현재 WebSocket 연결 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결이 종료되면 해당 그룹에서 연결 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # 클라이언트에서 메시지 받음
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']  # 메시지 보낸 사용자 정보

        if user.is_authenticated:
            sender = user.username
        else:
            sender = 'Anonymous'

        # 번역 챗봇 메시지 처리
        translated_text = await translate_text(message, target_lang=self.user_lang) # 예: 영어로 번역

        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': translated_text,
            'sender': '번역봇'
        }
        )

        # 그룹에 메시지를 전달
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender  # sender 정보 추가
            }
        )

    async def chat_message(self, event):
        # 메시지를 클라이언트로 전송
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'translated': event.get('translated', None),
            'sender': event['sender']  # 클라이언트로 보낼 때 sender 포함
        }))
