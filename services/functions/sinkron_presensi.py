import requests

from services.models import Configurations, TaskList

from .sinkron_sipo import ServiceSipo


class ServicePresensi:
    config = None
    next = None
    task_obj = None

    def __init__(self, task_id=None):
        self.config = Configurations.get_solo()
        if task_id:
            self.task_obj = TaskList.objects.get(id=task_id)

    def get_pegawai_list(self):
        url = "{}/api/v8/pegawai/simple/".format(self.config.presensi_url)
        if self.next:
            url = self.next
        response = requests.get(url, auth=("febriahmadn", "SegoPecel"), verify=False)
        if response.ok:
            response_json = response.json()
            results = response_json.get("results", None)
            self.next = response_json.get("next", None)
            if results:
                self.on_loop_results(results)
        return True

    def on_loop_results(self, results=[]):
        if len(results) > 0:
            for item in results:
                username = item.get("username", None)
                ServiceSipo().sinkron_pegawai_by_nip(username)
            if self.next:
                self.get_pegawai_list()
        return True
