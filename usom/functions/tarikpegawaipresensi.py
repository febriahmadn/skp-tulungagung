import requests
from usom.models import Account


class TarikPegawai:
    def proses(self):
        url = "http://localhost:9000/api/v8/pegawai/simple/"
        params = {}
        response = requests.get(url, params=params, auth=("febriahmadn", "SegoPecel"))
        print(response)
        if response.ok:
            results = response.json()
            # print(results)
            list_results = results.get("results", None)
            if list_results:
                for item in list_results:
                    print(item)
                    self.save(item)

        return True

    def save(self, item):
        username = item.get("username", None)
        nama_lengkap = item.get("nama_lengkap", None)

        account_list = Account.objects.filter(username=username)
        if account_list.exists():
            account_obj = account_list.last()
            account_obj.nama_lengkap = nama_lengkap
        else:
            # Create account
            account_obj = Account(username=username, nama_lengkap=nama_lengkap)
        account_obj.save()
        return item
