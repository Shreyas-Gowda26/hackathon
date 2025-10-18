from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from pydantic import EmailStr
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME="your_email@gmail.com",
    MAIL_PASSWORD="your_app_password",
    MAIL_FROM="your_email@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,   # ✅ replaces MAIL_TLS
    MAIL_SSL_TLS=False,   # ✅ replaces MAIL_SSL
)


async def send_email(subject:str, recipients:List[EmailStr],body:str):
    message = MessageSchema(
     subject=subject,
     recipients=recipients,
    body=body,
    subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)