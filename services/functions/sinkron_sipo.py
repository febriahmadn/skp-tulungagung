import re

import requests
from django.contrib.auth.models import Group

from services.models import Configurations
from usom.models import Account, Golongan, UnitKerja


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
            else:
                # print(response.status_code)
                if response.status_code in [500, 401]:
                    self.auth_login()
                    self.sinkron_pegawai_by_nip(nip)
                    return True
        return False

    def get_jabatan(self, payload):
        jabatan = payload.get("nama_jabatan", None)
        if jabatan:
            return re.sub(" +", " ", jabatan)
        return None

    def get_unitkerja(self, payload):
        nama_unitkerja = payload.get("unit_tugas", None)
        kode_unitkerja = payload.get("unit_tugas_kode", None)
        unitkerja_obj, created = UnitKerja.objects.get_or_create(
            id_sipo=kode_unitkerja, unitkerja=nama_unitkerja
        )

        if unitkerja_obj:
            return unitkerja_obj.id
        return None

    def get_golongan(self, payload):
        golongan = payload.get("gol_ruang", None)
        if golongan:
            if golongan.find("-") < 0:
                find_golongan = Golongan.objects.filter(kode=golongan)
                if find_golongan.exists():
                    return find_golongan.last()
        return None

    def get_eselon(self, payload):
        eselon = payload.get("eselon", None)
        if eselon:
            if eselon.find("-") < 0:
                eselon = eselon.replace(".", "-")
                return eselon.upper()
        return None

    def get_jenis_jabatan(self, payload):
        # JPT : eselon kode nya 21 dan 22
        # jenjab_kode nya 1
        # JA:
        # 1. eselon III dan IV jenjab: 1 eselon_kode: 31, 32, 41, 42
        # JA: Pelaksana
        # jenjab_kode : 4
        # JF:
        # jenjab_kode = 2

        eselon_kode = payload.get("eselon_kode", None)
        jenjab_kode = payload.get("jenjab_kode", None)
        jenis_jabatan = None
        if eselon_kode in ["21", "22"] and jenjab_kode == "1":
            jenis_jabatan = "JPT"
        elif eselon_kode in ["31", "32", "41", "42"] and jenjab_kode in ["1", "4"]:
            jenis_jabatan = "JA"
        elif jenjab_kode == "2":
            jenis_jabatan = "JF"
        return jenis_jabatan

    def handler_save(self, payload={}):
        if payload:
            try:
                data = {
                    "id_sipo": payload.get("id", None),
                    "username": payload.get("nip", None),
                    "nama_lengkap": payload.get("nama", None),
                    "gelar_depan": payload.get("glrdpn", None),
                    "gelar_belakang": payload.get("glrblk", None),
                    "is_staff": True,
                    "is_active": True,
                    "jabatan": self.get_jabatan(payload),
                    "unitkerja_id": self.get_unitkerja(payload),
                    "golongan": self.get_golongan(payload),
                    "eselon": self.get_eselon(payload),
                    "jenis_jabatan": self.get_jenis_jabatan(payload),
                }

                account_obj, created = Account.objects.get_or_create(
                    username=payload.get("nip", None)
                )

                if created:
                    account_obj.set_password("tulungagung2022")
                account_obj.save()

                for key, value in data.items():
                    setattr(account_obj, key, value)

                try:
                    group_input = Group.objects.get(name="Input")
                except Group.DoesNotExist:
                    print("Group Not Found")
                else:
                    account_obj.groups.add(group_input)
                    account_obj.save()
                return True
            except Exception as e:
                print(e)
        return False
