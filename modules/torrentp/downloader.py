from time import localtime

class Downloader:
    def __init__(self, session, torrent_info, save_path, libtorrent, is_magnet):
        self._session = session
        self._torrent_info = torrent_info
        self._save_path = save_path
        self._file = None
        self._status = None
        self._name = ''
        self._state = ''
        self._lt = libtorrent
        self._add_torrent_params = None
        self._is_magnet = is_magnet
        self._second = 0

    def status(self):
        if not self._is_magnet:
            self._file = self._session.add_torrent({'ti': self._torrent_info, 'save_path': f'{self._save_path}'})
            self._status = self._file.status()
        else:
            self._add_torrent_params = self._torrent_info
            self._add_torrent_params.save_path = self._save_path
            self._file = self._session.add_torrent(self._add_torrent_params)
            self._status = self._file.status()
        return self._status

    @property
    def name(self):
        self._name = self.status().name
        return self._name

    def download(self, sms):
        print(f'Start downloading {self.name}')
        while not self._status.is_seeding:
            s = self.status()
            
            if self._second % 3 == 0:
                try:
                    sms.edit_text('**\rComplete: `%.2f%%` \nDown: `%.1f kB/s` \nUp: `%.1f kB/s` \nPeers: `%d` \n__%s__**' % (
                        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                        s.num_peers, s.state))
                    self._second = 0
                except:
                    pass
                
            self._second = localtime().tm_sec

        sms.edit_text("✅ **Descarga completa**")
        print(self._status.name, 'downloaded successfully.')

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __call__(self):
        pass
