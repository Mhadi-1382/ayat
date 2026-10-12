from pusher_push_notifications import PushNotifications

INSTANCE_ID = '3ca35f8a-d0aa-428c-a10c-a3aeddf0da48'
SECRET_KEY = '653740728DE75F12FF091F18B20ED9DAF0CE7559DDDC8F8F446C37ED1E4D287C'

def config_notification(title, content, link):
    beams_client = PushNotifications(
        instance_id=INSTANCE_ID,
        secret_key=SECRET_KEY,
    )
    
    response = beams_client.publish_to_interests(
      interests=['Ayah'],
      publish_body={
        'web': {
          'notification': {
            'title': f'{title}',
            'body': f'{content}',
            'icon': 'https://ayat.chbkn.run/static/assets/images/logo/SVG/icon_splash.svg',
            'deep_link': f'{link}',
          },
        },
      },
    )
    
    print(response['publishId'])
