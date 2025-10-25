import requests, json
from tkinter import messagebox as msg
def send_message(source,message,to):
    try:
        username = 'Daenicel'
        api_key = '5E75107C-D1D5-0DFC-06A9-356BABB6FCBA'

        url = "https://rest.clicksend.com/v3/sms/send"
        headers = {
            "Content-Type": "application/json"
        }

        message_data = {
            "messages": [
                {
                    "source": source,
                    "from": 'python',
                    "body": message,
                    "to": to,

                }
            ]
        }
        
        response = requests.post(
            url,
            headers=headers,
            data= json.dumps(message_data),
            auth= (username, api_key)
        )

        if response.status_code == 200:
            msg.showinfo('sent',f'Message sent successfully: {response.json()}' )
        else:
            print('Error sending the message', response.status_code, response.text)
    except Exception as e:
        msg.showerror('Error',f'Please sign in to clicksend API to continue:    error: {e}')
                  



