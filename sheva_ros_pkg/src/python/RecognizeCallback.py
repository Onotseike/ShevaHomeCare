from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback



# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        self.transcribedText = ''
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        #print(transcript)
        pass

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Transcription completed')

    def on_hypothesis(self, hypothesis):
        print('hypothesis')
        self.transcribedText = hypothesis
       

    def on_data(self, data):
        #print(data')
        pass

    def GetTranscribedText(self):
        return self.transcribedText