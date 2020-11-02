# furo-de-audio

スマホやPC上で選んだSpotify上で再生できる曲、もしくはLocalに保存している曲を風呂場で楽しむことが出来る

Play a song list from Spotify on smartphone or local music server.

## User story

Spotify:
Playerがブラウザから曲を選択 -> Clientが選択された曲からHTTPrequestをつくる -> ServerがClientから送られてきたRequestをもとにSpotifyWebAPIを呼ぶ -> MusicStreamから曲がstreaming再生される

Local:
もしくはClientからリアルタイムで送信されるaudio(mp3/flac/etc)をServerがPCM形式に変換し、MusicStreamに再送信する -> MusicStreamでstreaming再生

## System environment

>### RaspberryPi3B+(Server)

* Frame_work: Node.js
* Database: PostgreSQL
* Verification & AcceptServer: Keycloak

>### RaspberryPi3B+(MusicStream)

* Programming language: Java8
* Software for streaming songs in Spotify: Raspotify

>### Player(Client)

* Browser
* HTML,CSS,Javascript

## Feature

* 風呂場でAudioを楽しめる
* Spotifyの曲を再生できる
* Localにある曲を再生可能(mp3/flac/etc)
* SpotifyのPlaylistや履歴からAIがUserごとにRecommendを作成

## Layout

### Screenshotが入る

## References

* raspotify: https://github.com/dtcooper/raspotify