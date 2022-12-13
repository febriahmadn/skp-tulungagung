def string_to_int(cls, the_string):
    """Convert the string value to an int value, or return None."""
    for num, string in cls.choices:
        if string == the_string:
            return num
    return None


FULL_BULAN = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}


def get_predikat_kerja(rating_obj, predikat_obj):
    if (
        rating_obj.nama == "Dibawah Ekspetasi"
        and predikat_obj.nama == "Dibawah Ekspetasi"
    ):
        return "SANGAT KURANG"
    elif (
        rating_obj.nama == "Dibawah Ekspetasi"
        and predikat_obj.nama == "Sesuai Ekspetasi"
    ):
        return "BUTUH PERBAIKAN"
    elif (
        rating_obj.nama == "Dibawah Ekspetasi"
        and predikat_obj.nama == "Diatas Ekspetasi"
    ):
        return "BUTUH PERBAIKAN"
    elif (
        rating_obj.nama == "Sesuai Ekspetasi"
        and predikat_obj.nama == "Dibawah Ekspetasi"
    ):
        return "KURANG"
    elif (
        rating_obj.nama == "Sesuai Ekspetasi"
        and predikat_obj.nama == "Sesuai Ekspetasi"
    ):
        return "BAIK"
    elif (
        rating_obj.nama == "Sesuai Ekspetasi"
        and predikat_obj.nama == "Diatas Ekspetasi"
    ):
        return "BAIK"
    elif (
        rating_obj.nama == "Diatas Ekspetasi"
        and predikat_obj.nama == "Dibawah Ekspetasi"
    ):
        return "KURANG"
    elif (
        rating_obj.nama == "Diatas Ekspetasi"
        and predikat_obj.nama == "Sesuai Ekspetasi"
    ):
        return "BAIK"
    elif (
        rating_obj.nama == "Diatas Ekspetasi"
        and predikat_obj.nama == "Diatas Ekspetasi"
    ):
        return "SANGAT BAIK"
    else:
        return None
