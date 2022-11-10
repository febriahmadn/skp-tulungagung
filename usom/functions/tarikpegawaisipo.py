import requests
from usom.models import Account


class TarikPegawaiSipo:

    def sync(self):
        akun_list = Account.objects.all()
        for item in akun_list:
            self.proses(item.username)

    def proses(self, nip=None):
        url = 'https://sipo.bkd.tulungagung.go.id/web/index.php'
        params = {
            'r': 'api/pns',
            'access_token': '79B00E729FCCA845C29E318AC377EB6C38E19A6009371107377AEE161A666233',
        }

        if nip:
            params.update({
                'nip': nip
            })

        response = requests.get(url, params=params)
        if response.ok:
            results = response.json()
            # list_results = results.get('results')
            # if results.exists():
            for item in results:
                # print(item)
                self.save(item)

    def save(self, item):
        nip = item.get('nip', None)
        account_list = Account.objects.filter(
            username=nip
        )
        print(account_list)
