from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.helpers import frontend_url, esperar, limpiar_sesion, LONG_TEXT


class TestLogin:

    def test_login_exitoso(self, driver):
        # print(driver)
        limpiar_sesion(driver)
        driver.get(frontend_url("login.html"))

        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        esperar(driver).until(EC.url_contains("index.html"))
        assert "index.html" in driver.current_url

    def test_login_credenciales_incorrectas(self, driver):
        limpiar_sesion(driver)
        # print(driver.current_url)
        driver.get(frontend_url("login.html"))

        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("clave_erronea_123")
        driver.find_element(By.ID, "send").click()

        alerta = esperar(driver).until(EC.visibility_of_element_located((By.ID, "alert")))
        assert alerta.is_displayed()
        assert len(alerta.text) > 0

    def test_login_usuario_limite_maximo(self, driver):
        limpiar_sesion(driver)
        driver.get(frontend_url("login.html"))
        # print(driver.current_url)

        driver.find_element(By.ID, "username").send_keys(LONG_TEXT)
        driver.find_element(By.ID, "password").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alerta = esperar(driver).until(EC.visibility_of_element_located((By.ID, "alert")))
        assert alerta.is_displayed()
