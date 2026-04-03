from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.helpers import (
    esperar, ir_a_index, asegurar_al_menos_un_registro,
    guardar_modal, cancelar_modal,
)


class TestEditarRegistro:

    def test_editar_registro_exitoso(self, driver):
        ir_a_index(driver)
        asegurar_al_menos_un_registro(driver)

        driver.find_element(By.XPATH, "(//button[text()='Editar'])[1]").click()
        esperar(driver).until(EC.visibility_of_element_located((By.ID, "crmModal")))

        campo = driver.find_element(By.ID, "customerName")
        campo.clear()
        campo.send_keys("Cliente Editado OK")
        guardar_modal(driver)

        esperar(driver).until(
            EC.text_to_be_present_in_element((By.ID, "tableBody"), "Cliente Editado OK")
        )
        assert "Cliente Editado OK" in driver.find_element(By.ID, "tableBody").text

    def test_editar_cancelar_no_guarda_cambios(self, driver):
        ir_a_index(driver)
        asegurar_al_menos_un_registro(driver)

        nombre_original = driver.find_elements(
            By.CSS_SELECTOR, "#tableBody tr td:nth-child(2)"
        )[0].text

        driver.find_element(By.XPATH, "(//button[text()='Editar'])[1]").click()
        esperar(driver).until(EC.visibility_of_element_located((By.ID, "crmModal")))

        campo = driver.find_element(By.ID, "customerName")
        campo.clear()
        campo.send_keys("Nombre Que No Se Guarda")
        cancelar_modal(driver)

        esperar(driver).until(EC.invisibility_of_element_located((By.ID, "crmModal")))

        nombre_actual = driver.find_elements(
            By.CSS_SELECTOR, "#tableBody tr td:nth-child(2)"
        )[0].text
        assert nombre_actual == nombre_original

    def test_editar_campo_nombre_vacio_muestra_advertencia(self, driver):
        ir_a_index(driver)
        asegurar_al_menos_un_registro(driver)

        driver.find_element(By.XPATH, "(//button[text()='Editar'])[1]").click()
        esperar(driver).until(EC.visibility_of_element_located((By.ID, "crmModal")))

        driver.find_element(By.ID, "customerName").clear()
        guardar_modal(driver)

        alerta = esperar(driver).until(EC.visibility_of_element_located((By.ID, "alert")))
        assert "Completa todos los campos" in alerta.text
