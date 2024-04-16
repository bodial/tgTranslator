from telethon.sync import TelegramClient
from telethon import events
from pydub import AudioSegment
import speech_recognition as sr
import config

def convert_audio_to_wav(input_file, output_file):
    audio = AudioSegment.from_ogg(input_file)
    audio.export(output_file, format="wav")
    return output_file


# Функция для распознавания речи
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            return text
        except sr.UnknownValueError:
            print("Речь не распознана")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания речи")
            return None


input_file = 'voice_message.ogg'
output_file = 'voice_message.wav'


# Авторизация в Telegram
client = TelegramClient('session', config.api_id, config.api_hash, timeout=None)

@client.on(events.NewMessage)
async def normal_handler(event):

    msgDict = event.message.to_dict()
    print('message')
    print(msgDict)

    if (msgDict['media'] and msgDict['media']['voice']) is not None:
        try:
            print('voice')
            await event.download_media(input_file)

            # Конвертируем аудио в wav
            wav_file = convert_audio_to_wav(input_file, output_file)

            # Распознаем речь и выводим текст в консоль
            text = recognize_speech(wav_file)
            if text:
                print("Распознанный текст:", text)
                await event.message.reply('Распознанный текст: ' + text)
            else:
                await event.message.reply('Сообщение не распознано')
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")



async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


