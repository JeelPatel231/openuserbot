import libtorrent as lt
import time
import shutil
from datetime import datetime
from telethon import events
import os
from userbot import CMD_HELP


#start libtorrent download
ses = lt.session()
ses.listen_on(6881, 6891)
params = {
    'save_path': '/root/userbot/Torrent/',
    'storage_mode': lt.storage_mode_t(2),
    'paused': False,
    'auto_managed': True,
    'duplicate_is_error': True}
link = "" # PASTE TORRENT/MAGNET LINK HERE
print(link)

handle = lt.add_magnet_uri(ses, link, params)
ses.start_dht()

begin = time.time()
print(datetime.datetime.now())

print ('Downloading Metadata...')
while (not handle.has_metadata()):
    time.sleep(1)
print ('Got Metadata, Starting Torrent Download...')

print("Starting", handle.name())

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()
    state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
    print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETE")

print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")

print(datetime.datetime.now())
#end lib torrent download


#start zipping
shutil.make_archive(handle.name(), 'zip', '/root/userbot/torrent/'+handle.name())
#end zipping

#send
#bot.send_document(chat_id, file=open(/root/userbot/torrent/handle.name()+".zip"))
#sent

#deleting
#if os.path.exists('/root/userbot/'+handle.name()+".zip"):
#  os.remove('/root/userbot/'handle.name()+".zip")
#  shutil.rmtree('/root/userbot/torrent/handle.name()')
#else:
#  print("The file does not exist")
#

CMD_HELP.update({"torrent": ".torrent\
\nUsage: .torrent (paste magnet link here)"})
