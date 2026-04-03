from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.helpers import frontend_url, esperar, limpiar_sesion, ir_a_index


class TestVerLista:

    def test_ver_lista_con_datos(self, driver):
        ir_a_index(driver)
        tbody = driver.find_element(By.ID, "tableBody")
        assert tbody.is_displayed()

    def test_lista_sin_autenticacion_redirige(self, driver):
        # print(driver.current_url)

        limpiar_sesion(driver)
        driver.get(frontend_url("index.html"))
        esperar(driver).until(EC.url_contains("login.html"))
        assert "login.html" in driver.current_url

    def test_tabla_tiene_seis_columnas(self, driver):
        ir_a_index(driver)
        columnas = driver.find_elements(By.CSS_SELECTOR, "thead th")
        assert len(columnas) == 6
