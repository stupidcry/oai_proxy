from flask import Blueprint, request,send_file
import azure.cognitiveservices.speech as speechsdk
import logging
import io
import time

speech_key, service_region = "EkRhgUL5IbdoHSxXDn9aKM0nQPbgmuScNk1OGac5ZeZ9M8LuKVh4JQQJ99BAACqBBLyXJ3w3AAAYACOGQgFb", "southeastasia"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
# zh-CN-XiaoxiaoMultilingualNeural
# zh-CN-Xiaochen:DragonHDLatestNeural  500k
# zh-CN-XiaochenMultilingualNeural
speech_config.speech_synthesis_voice_name = "zh-CN-XiaochenMultilingualNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=None)

azure_module = Blueprint('azure_module', __name__)

def synthesize_speech(text):
    result = speech_synthesizer.speak_text_async(text).get()
    return io.BytesIO(result.audio_data)

@azure_module.route('/tts', methods=['POST'])
def tts_az():
    text = request.json.get('text')
    if not text:
        return "Missing text parameter", 400
    
    # 合成语音并获取音频数据
    start_time = time.time()
    
    audio_stream = synthesize_speech(text)
    logging.debug(f"time：{time.time()-start_time}")
    if audio_stream:
        return send_file(audio_stream, mimetype='audio/wav', as_attachment=True,download_name="out.wav")
    else:
        return "Failed to synthesize speech", 500