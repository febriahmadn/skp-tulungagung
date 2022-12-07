import re
import requests
from services.models import Configurations
from usom.models import Account, UnitKerja


class ServiceSipo:
    config = None
    token = None

    def __init__(self):
        self.config = Configurations.get_solo()
        self.token = self.config.sipo_token

    def auth_login(self):
        payload = {
            "LoginForm[username]": self.config.sipo_username,
            "LoginForm[password]": self.config.sipo_password,
        }
        url = self.config.sipo_url + "?r=auth/login"
        response = requests.request("POST", url, data=payload)
        if response.ok:
            results = response.json()
            token = results.get("token", None)
            self.token = token
            self.config.sipo_token = token
            self.config.save()
        return True

    def sinkron_pegawai_by_nip(self, nip=None):
        if nip:
            if self.token is None or self.token == "":
                self.auth_login()
            url = self.config.sipo_url
            params = {"r": "api/pns", "nip": nip}
            headers = {"Authorization": "Bearer {}".format(self.token)}
            response = requests.request("GET", url, params=params, headers=headers)
            if response.ok:
                results = response.json()
                if len(results) > 0:
                    self.handler_save(results[0])
                return True
        return False

    def handler_save(self, payload={}):
        if payload:
            # print(payload)
            data = {
                "id_sipo": payload.get("id", None),
                "username": payload.get("nip", None),
                "nama_lengkap": payload.get("nama", None),
                "gelar_depan": payload.get("glrdpn", None),
                "gelar_belakang": payload.get("glrblk", None),
                "is_staff": True,
                "is_active": True,
            }

            jabatan = payload.get("nama_jabatan", None)
            if jabatan:
                data.update({"jabatan": re.sub(" +", " ", jabatan)})

            nama_unitkerja = payload.get("unit_tugas", None)
            kode_unitkerja = payload.get("unit_tugas_kode", None)

            unitkerja_obj, created = UnitKerja.objects.get_or_create(
                id_sipo=kode_unitkerja, unitkerja=nama_unitkerja
            )

            if unitkerja_obj:
                data.update({"unitkerja_id": unitkerja_obj.id})

            account_obj, created = Account.objects.get_or_create(
                username=payload.get("nip", None)
            )

            for key, value in data.items():
                setattr(account_obj, key, value)
            account_obj.save()
            print(data)
