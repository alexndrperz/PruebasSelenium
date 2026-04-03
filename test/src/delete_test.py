from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.helpers import esperar, ir_a_index, asegurar_al_menos_un_registro, js_click


class TestEliminarRegistro:

    def test_eliminar_registro_exitoso(self, driver):
        ir_a_index(driver)
        # print("llegue")
        asegurar_al_menos_un_registro(driver)

        filas_antes = len(driver.find_elements(By.CSS_SELECTOR, "#tableBody tr"))

        btn = driver.find_element(By.XPATH, "(//button[text()='Eliminar'])[1]")
        js_click(driver, btn)
        driver.switch_to.alert.accept()

        def fila_eliminada(d):
            filas = len(d.find_elements(By.CSS_SELECTOR, "#tableBody tr"))
            return filas < filas_antes or "Sin registros" in d.find_element(By.ID, "tableBody").text

        esperar(driver).until(fila_eliminada)

        filas_despues = len(driver.find_elements(By.CSS_SELECTOR, "#tableBody tr"))
        assert filas_despues < filas_antes or "Sin registros" in driver.find_element(By.ID, "tableBody").text

    def test_eliminar_cancelar_mantiene_registro(self, driver):
        ir_a_index(driver)
        asegurar_al_menos_un_registro(driver)

        filas_antes = len(driver.find_elements(By.CSS_SELECTOR, "#tableBody tr"))

        btn = driver.find_element(By.XPATH, "(//button[text()='Eliminar'])[1]")
        # print(btn.get_attribute("id"))
        js_click(driver, btn)
        driver.switch_to.alert.dismiss()

        filas_despues = len(driver.find_elements(By.CSS_SELECTOR, "#tableBody tr"))
        assert filas_despues == filas_antes

    def test_eliminar_ultimo_registro_muestra_estado_vacio(self, driver):
        ir_a_index(driver)
        asegurar_al_menos_un_registro(driver)

        while True:
            btns = driver.find_elements(By.XPATH, "//button[text()='Eliminar']")
            if not btns:
                break
            cantidad = len(btns)
            js_click(driver, btns[0])
            driver.switch_to.alert.accept()
            # print(btns[0].get_attribute("id"))
            def botones_reducidos(d):
                n = len(d.find_elements(By.XPATH, "//button[text()='Eliminar']"))
                return n < cantidad or "Sin registros" in d.find_element(By.ID, "tableBody").text

            esperar(driver).until(botones_reducidos)

            if "Sin registros" in driver.find_element(By.ID, "tableBody").text:
                break

        assert "Sin registros" in driver.find_element(By.ID, "tableBody").text
