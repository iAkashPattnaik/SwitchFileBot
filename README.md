<h1 align="center">🗃️ SwitchFileBot</h1>

A simple bot which can be used to share files along with metadata between [telegram](https://telegram.dog) and [[switch android](https://play.google.com/store/apps/details?id=com.app.switchapp1) or [switch apple](https://apps.apple.com/in/app/switch-chats-and-communities/id1640630735)] on a temorary id basis for 24 hours.

## How it works?

- You send a file to either the _[telegram bot](https://t.me/SwitchFileBot)_ or _[switch bot](https://myswitch.click/ELHC)_.
- The `file_data` is registred into `mongodb` database.
- A `fetch_id` is generated which is valid for 24 hours.
- Anyone can get the file using this `fetch_id` on either of the bots.

> ⚠️ Switch is still under development.

## TODO

- [ ] Use match-case rather than if-else in `telegram_bot/main.py:fetch_command`
- [ ] Add force_sub for switch community
- [ ] Make the temporary file store time **custom**
- [ ] Add media broadcast

### Switch on Windows?

It's technically possible but you must have Windows 11 and [WSA](https://learn.microsoft.com/en-us/windows/android/wsa/) enabled.

Follow [this article](https://ahaan.co.uk/article/top_stories/google-play-store-windows-11-install) and you can install any google playstore app in windows!