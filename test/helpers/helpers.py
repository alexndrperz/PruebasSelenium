from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_DIR = Path(__file__).parent.parent.parent / "src" / "frontend"
LONG_TEXT = "A" * 50


def frontend_url(page: str) -> str:
    return (FRONTEND_DIR / page).as_uri()


def esperar(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def tabla_lista(d):
    return "Cargando" not in d.find_element(By.ID, "tableBody").text


def establecer_sesion(driver):
    driver.get(frontend_url("login.html"))
    driver.execute_script("localStorage.setItem('user', 'admin')")


def limpiar_sesion(driver):
    driver.get(frontend_url("login.html"))
    driver.execute_script("localStorage.removeItem('user')")


def ir_a_index(driver):
    establecer_sesion(driver)
    driver.get(frontend_url("index.html"))
    esperar(driver).until(tabla_lista)


def abrir_modal_nuevo(driver):
    driver.find_element(By.XPATH, "//button[contains(text(),'Nuevo registro')]").click()
    esperar(driver).until(EC.visibility_of_element_located((By.ID, "crmModal")))


def llenar_formulario(driver, nombre, telefono, mensaje):
    driver.find_element(By.ID, "customerName").send_keys(nombre)
    driver.find_element(By.ID, "phone").send_keys(telefono)
    driver.find_element(By.ID, "message").send_keys(mensaje)


def guardar_modal(driver):
    driver.find_element(By.XPATH, "//div[@id='crmModal']//button[text()='Guardar']").click()


def cancelar_modal(driver):
    driver.find_element(By.XPATH, "//div[@id='crmModal']//button[text()='Cancelar']").click()


def crear_registro(driver, nombre="Registro Test", tel="5500000000", msg="Mensaje test"):
    abrir_modal_nuevo(driver)
    llenar_formulario(driver, nombre, tel, msg)
    guardar_modal(driver)
    esperar(driver).until(EC.text_to_be_present_in_element((By.ID, "tableBody"), nombre))


def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", element)


def asegurar_al_menos_un_registro(driver):
    tbody = driver.find_element(By.ID, "tableBody")
    if "Sin registros" in tbody.text or not driver.find_elements(By.XPATH, "//button[text()='Editar']"):
        crear_registro(driver)
