from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.helpers import (
    esperar, ir_a_index, abrir_modal_nuevo,
    llenar_formulario, guardar_modal, LONG_TEXT,
)


class TestCrearRegistro:

    def test_crear_registro_exitoso(self, driver):
        ir_a_index(driver)
        abrir_modal_nuevo(driver)
        llenar_formulario(driver, "Cliente Nuevo", "5511112222", "Mensaje de prueba")
        guardar_modal(driver)

        esperar(driver).until(
            EC.text_to_be_present_in_element((By.ID, "tableBody"), "Cliente Nuevo")
        )
        assert "Cliente Nuevo" in driver.find_element(By.ID, "tableBody").text

    def test_crear_sin_datos_muestra_advertencia(self, driver):
        ir_a_index(driver)
        abrir_modal_nuevo(driver)
        guardar_modal(driver)

        alerta = esperar(driver).until(
            EC.visibility_of_element_located((By.ID, "alert"))
        )
        assert "Completa todos los campos" in alerta.text

    def test_crear_con_texto_maximo(self, driver):
        # print(driver.current_url)
        ir_a_index(driver)
        abrir_modal_nuevo(driver)
        llenar_formulario(driver, LONG_TEXT, "9999999999", LONG_TEXT)
        guardar_modal(driver)

        esperar(driver).until(
            EC.text_to_be_present_in_element((By.ID, "tableBody"), LONG_TEXT[:20])
        )
        assert LONG_TEXT[:20] in driver.find_element(By.ID, "tableBody").text
