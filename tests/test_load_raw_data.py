import load_raw_data as loader
import pytest

COLUMNS = ["id", "name"]


def write(path, text):
    path.write_text(text, encoding="utf-8")


def test_read_csv_valido(tmp_path):
    write(tmp_path / "t.csv", "id,name\n1,ana\n2,luis\n")
    assert loader.read_csv("t.csv", COLUMNS, tmp_path) == [("1", "ana"), ("2", "luis")]


def test_read_csv_archivo_inexistente(tmp_path):
    with pytest.raises(loader.ValidationError, match="no existe"):
        loader.read_csv("falta.csv", COLUMNS, tmp_path)


def test_read_csv_columna_ausente(tmp_path):
    write(tmp_path / "t.csv", "id,otra\n1,x\n")
    with pytest.raises(loader.ValidationError, match="faltan columnas"):
        loader.read_csv("t.csv", COLUMNS, tmp_path)


def test_read_csv_solo_cabecera(tmp_path):
    write(tmp_path / "t.csv", "id,name\n")
    with pytest.raises(loader.ValidationError, match="no contiene filas"):
        loader.read_csv("t.csv", COLUMNS, tmp_path)


def test_read_csv_linea_incompleta(tmp_path):
    write(tmp_path / "t.csv", "id,name\n1\n")
    with pytest.raises(loader.ValidationError, match="menos campos"):
        loader.read_csv("t.csv", COLUMNS, tmp_path)


def test_main_no_toca_la_bd_si_falla_la_validacion(tmp_path, monkeypatch):
    # carpeta vacía: ningún CSV existe, así que la validación debe fallar
    monkeypatch.setattr(loader, "RAW_DIR", tmp_path)

    def no_deberia_conectar(*args, **kwargs):
        raise AssertionError("main() no debe abrir conexión si la validación falla")

    monkeypatch.setattr(loader.psycopg, "connect", no_deberia_conectar)

    assert loader.main() == 1
