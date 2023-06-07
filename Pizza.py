from flask import Flask
app = Flask(__name__)
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage,TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate,PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn,ImageCarouselTemplate, ImageCarouselColumn
from urllib.parse import parse_qsl
line_bot_api = LineBotApi('HoCWgxj9lhWPeTho1NgFf2ZCwc5TMCg5K6ScSwMEq9aKwqrxaFAX/oQKCB3FIxxkm8YPoUkJRs2ucji0YQeTiYya9oWTPwZhe1Nm29+l+oZtSrWw4kLnmrfvDC8onhuNsRyxvwsBeitjznPuHaYfdwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('07c250b43887f9f152a38e22d2bc53c3')
@app.route("/callback", methods=['POST'])
def callback():
     signature = request.headers['X-Line-Signature']
     body = request.get_data(as_text=True)
     try:
         handler.handle(body, signature)
     except InvalidSignatureError:
         abort(400)
     return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
     mtext = event.message.text
     if mtext == '@聯絡我們':
         sendButton(event)
     elif mtext == '@確認':
         sendConfirm(event)
     elif mtext == '@點餐':
         sendCarousel(event)
     elif mtext == '@新活動':
         sendImgCarousel(event)
     elif mtext == '@購買披薩':
         sendPizza(event)
     elif mtext == '@yes':
         sendYes(event)
@handler.add(PostbackEvent) #PostbackTemplateAction 觸發此事件
def handle_postback(event):
     backdata = dict(parse_qsl(event.postback.data)) #取得 Postback 資料
     if backdata.get('action') == 'buy':
         sendBack_buy(event, backdata)
     elif backdata.get('action') == 'sell':
         sendBack_sell(event, backdata)
def sendButton(event): #按鈕樣版
 try:
     message = TemplateSendMessage(
     alt_text='按鈕樣板',
     template=ButtonsTemplate(
     thumbnail_image_url='https://imgur.com/AiTQocb', #顯示的圖片
     title='我們的資訊', #主標題
     text='請選擇：', #副標題
     actions=[
     URITemplateAction( #開啟網頁
     label='連結網頁',
     uri='http://www.e-happy.com.tw'
     ),
     MessageTemplateAction( 
     label='電話', #按鈕文字
     text='XXXXXXXXXX', #顯示文字訊息
#     data='action=buy' #Postback 資料
     ),
     ]
     )
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendConfirm(event): #確認樣板
 try:
     message = TemplateSendMessage(
     alt_text='確認樣板',
     template=ConfirmTemplate(
     text='你確定要購買這項商品嗎？',
     actions=[
     MessageTemplateAction( #按鈕選項
     label='是',
     text='@yes'
     ),
     MessageTemplateAction(
     label='否',
     text='@no'
     )
     ]
     )
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendCarousel(event): #轉盤樣板
 try:
     message = TemplateSendMessage(
     alt_text='轉盤樣板',
     template=CarouselTemplate(
     columns=[
     CarouselColumn(
     thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
     title='Pizza',
     text='訂購pizza',
     actions=[
     MessageTemplateAction(
     label='訂購!',
     text='已幫您加入購物車'
     ),
     PostbackTemplateAction(
     label='回傳訂單',
     data='action=sell&item=披薩'
     ),
     ]
     ),
     CarouselColumn(
     thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
     title='Drink',
     text='訂購drink',
     actions=[
     MessageTemplateAction(
     label='訂購!',
     text='已幫您加入購物車'
     ),
     PostbackTemplateAction(
     label='回傳訂單',
     data='action=sell&item=飲料'
     ),
     ]
     )
     ]
     )
     )
     line_bot_api.reply_message(event.reply_token,message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendImgCarousel(event): #圖片轉盤
 try:
     message = TemplateSendMessage(
     alt_text='圖片轉盤樣板',
     template=ImageCarouselTemplate(
     columns=[
     ImageCarouselColumn(
     image_url='https://i.imgur.com/4QfKuz1.png',
     action=PostbackTemplateAction(
     label='訊息一',
     data='action=sell&item=披薩'
     )
     ),
     ImageCarouselColumn(
     image_url='https://i.imgur.com/qaAdBkR.png',
     action=PostbackTemplateAction(
     label='訊息二',
     data='action=sell&item=飲料'
     )
     )
     ]
     )
     )
     line_bot_api.reply_message(event.reply_token,message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendPizza(event):
 try:
     message = TextSendMessage(
     text = '感謝您購買披薩，我們將盡快為您製作。'
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendYes(event):
 try:
     message = TextSendMessage(
     text='感謝您的購買，\n 我們將盡快寄出商品。',
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendBack_buy(event, backdata): #處理 Postback
 try:
     text1 = '以下是您選購的商品：' +backdata.get('action') + ')'
     message = TextSendMessage( #傳送文字
     text = text1
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendBack_sell(event, backdata): #處理 Postback
 try:
     message = TextSendMessage( #傳送文字
     text = '點選的是活動' + backdata.get('item')
     )
     line_bot_api.reply_message(event.reply_token, message)
 except:
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
if __name__ == '__main__':
 app.run()
