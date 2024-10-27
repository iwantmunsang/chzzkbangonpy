from winotify import Notification , audio

toast = Notification(app_id= "치지직뱅온알람",
                                         title="{name}",
                                         msg="{name}님이 방송중 입니다!!\n제목 : {strimingname}",
                                         icon= r"C:\Users\a0109\Desktop\chzzkbangonpy\chzzkbangonpy\images\MDAxNzAyOTA1MjY1NTM1.kBdadHp17ATBAt5XbaeIxdlw2AYgFCdGkoQP6JJW8pEg.cRpnPw04hOQcFXVer1-nABzDip9lwhZt_WyMOs1zzPgg.JPEG",
                                         duration= "short")
toast.add_actions(label="방송 보러가기", launch="https://chzzk.naver.com/4f3626031d1ff12931a34242a7f6900f")
toast.set_audio(audio.Default, loop=False)
toast.show()